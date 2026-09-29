/**
 * translator.worker.js
 * Dedicated Web Worker for offline NLLB-200 translation with WebGPU/WASM support.
 */
import { pipeline, env } from "@huggingface/transformers";

// FLORES-200 language code mappings for the 6 supported Indian languages
export const LANGUAGE_CODES = {
  hi: { code: "hin_Deva", name: "Hindi", native: "हिन्दी" },
  ta: { code: "tam_Taml", name: "Tamil", native: "தமிழ்" },
  te: { code: "tel_Telu", name: "Telugu", native: "తెలుగు" },
  bn: { code: "ben_Beng", name: "Bengali", native: "বাংলা" },
  mar: { code: "mar_Deva", name: "Marathi", native: "मराठी" },
  gu: { code: "guj_Gujr", name: "Gujarati", native: "ગુજરાતી" },
};

export const SOURCE_LANG_CODE = "eng_Latn"; // English

/**
 * Singleton class to manage the Translation Pipeline instance
 */
class TranslationPipelineSingleton {
  static task = "translation";
  static model = "Xenova/nllb-200-distilled-600M";
  static instance = null;
  static activeDevice = "wasm";

  static async getInstance(config = {}, progressCallback = null) {
    if (this.instance === null) {
      const { isDesktop = false, localModelPath = "/models/" } = config;

      // 1. Configure environment paths for Web PWA vs Desktop (Tauri/Electron)
      if (isDesktop) {
        env.allowLocalModels = true;
        env.allowRemoteModels = false;
        env.localModelPath = localModelPath;
      } else {
        // Web / PWA mode: use browser cache API
        env.allowLocalModels = false;
        env.allowRemoteModels = true;
        env.useBrowserCache = true;
      }

      // 2. Determine execution device: WebGPU with graceful WASM fallback
      let device = "wasm";
      if (typeof navigator !== "undefined" && "gpu" in navigator) {
        try {
          const adapter = await navigator.gpu.requestAdapter();
          if (adapter) {
            device = "webgpu";
          }
        } catch {
          device = "wasm";
        }
      }
      this.activeDevice = device;

      // 3. Initialize translation pipeline with 8-bit quantized weights (q8)
      this.instance = await pipeline(this.task, this.model, {
        device: this.activeDevice,
        dtype: "q8",
        progress_callback: progressCallback,
      });
    }
    return this.instance;
  }
}

// Global active request tracker to allow canceling obsolete keystroke requests
let currentRequestId = 0;

self.addEventListener("message", async (event) => {
  const { type, payload } = event.data;

  if (type === "INIT") {
    const { isDesktop, localModelPath } = payload || {};
    try {
      self.postMessage({ status: "loading", message: "Initializing translation engine..." });

      await TranslationPipelineSingleton.getInstance(
        { isDesktop, localModelPath },
        (progress) => {
          self.postMessage({
            status: "progress",
            progress: progress,
          });
        }
      );

      self.postMessage({
        status: "ready",
        device: TranslationPipelineSingleton.activeDevice,
        message: "Translation engine is ready and offline-capable.",
      });
    } catch (error) {
      self.postMessage({
        status: "error",
        error: error.message || "Failed to initialize translation model.",
      });
    }
  }

  if (type === "TRANSLATE") {
    const { id, text, targetLang } = payload;
    currentRequestId = id;

    if (!text || text.trim() === "") {
      self.postMessage({
        status: "complete",
        id,
        output: "",
        targetLang,
        latencyMs: 0,
      });
      return;
    }

    const tgtLangCode = LANGUAGE_CODES[targetLang]?.code || targetLang;

    try {
      self.postMessage({ status: "translating", id });
      const startTime = performance.now();

      const translator = await TranslationPipelineSingleton.getInstance();

      // Check if another keystroke superseded this request while waiting
      if (id !== currentRequestId) {
        return;
      }

      const output = await translator(text, {
        src_lang: SOURCE_LANG_CODE,
        tgt_lang: tgtLangCode,
        max_new_tokens: 256,
      });

      const latencyMs = Math.round(performance.now() - startTime);
      const translatedText = output?.[0]?.translation_text || "";

      // Post result if request is still the freshest
      if (id === currentRequestId) {
        self.postMessage({
          status: "complete",
          id,
          output: translatedText,
          targetLang,
          latencyMs,
          device: TranslationPipelineSingleton.activeDevice,
        });
      }
    } catch (error) {
      if (id === currentRequestId) {
        self.postMessage({
          status: "error",
          id,
          error: error.message || "Error occurred during translation.",
        });
      }
    }
  }
});
