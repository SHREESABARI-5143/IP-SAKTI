'use client';

import React, { useState, useEffect } from 'react';
import { Lock, Upload, FileText, CheckCircle2, Shield, AlertCircle } from 'lucide-react';
import { api } from '@/lib/api';

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [successMsg, setSuccessMsg] = useState('');

  const fetchDocs = async () => {
    setLoading(true);
    try {
      const data = await api.getDocuments();
      setDocuments(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocs();
  }, []);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    setSuccessMsg('');
    try {
      const fd = new FormData();
      fd.append('file', file);
      fd.append('jurisdiction', 'India');
      fd.append('domain', 'Proprietary Research');

      const res = await api.uploadDocument(fd);
      setSuccessMsg(res.message);
      setFile(null);
      fetchDocs();
    } catch (err) {
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header */}
      <div className="border-b border-slate-200 pb-4">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-100 text-slate-800 text-xs font-bold mb-2">
          <Lock className="w-4 h-4 text-slate-600" />
          Isolated Tenant Document Vault (Private RAG)
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Private Knowledge & Proprietary Dossiers
        </h1>
        <p className="text-sm text-slate-600 mt-1">
          Upload proprietary formulation dossiers, laboratory test reports, and patent drafts. Documents are parsed and indexed in an isolated <code className="text-teal-700 font-mono">PRIVATE_USER_DOCUMENTS</code> namespace with zero data leakage.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Upload Form */}
        <div className="lg:col-span-5 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Upload Private Document</h2>

          <form onSubmit={handleUpload} className="space-y-4 text-xs">
            <div className="border-2 border-dashed border-slate-300 hover:border-teal-500 rounded-2xl p-6 text-center transition-all bg-slate-50/50">
              <Upload className="w-8 h-8 text-teal-600 mx-auto mb-2" />
              <p className="font-semibold text-slate-700">
                {file ? file.name : 'Choose a PDF, DOCX, or TXT file'}
              </p>
              <p className="text-[11px] text-slate-500 mt-1">
                Max file size: 25MB. Text extraction and vector chunking happen securely.
              </p>
              <input
                type="file"
                accept=".pdf,.docx,.txt,.csv"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="mt-3 block w-full text-[11px] text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-teal-700 hover:file:bg-teal-100 cursor-pointer"
              />
            </div>

            {successMsg && (
              <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-lg flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
                <span className="font-semibold">{successMsg}</span>
              </div>
            )}

            <button
              type="submit"
              disabled={!file || uploading}
              className="w-full py-2.5 bg-teal-700 hover:bg-teal-800 disabled:opacity-40 text-white font-semibold rounded-xl flex items-center justify-center gap-2 shadow-sm transition-all"
            >
              <span>{uploading ? 'Parsing & Indexing...' : 'Securely Index Document'}</span>
            </button>
          </form>
        </div>

        {/* Document List */}
        <div className="lg:col-span-7 space-y-4">
          <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
            Indexed Private Documents ({documents.length})
          </h2>

          {loading ? (
            <div className="p-8 text-center text-xs text-slate-500">Loading documents...</div>
          ) : documents.length === 0 ? (
            <div className="p-8 bg-white border border-slate-200 rounded-2xl text-center text-slate-400 space-y-2">
              <FileText className="w-10 h-10 text-slate-300 mx-auto" />
              <p className="text-xs font-semibold text-slate-700">No private documents uploaded yet</p>
              <p className="text-[11px] text-slate-500">
                Uploaded dossiers will automatically enhance your conversational Copilot answers while remaining strictly private.
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {documents.map((doc) => (
                <div key={doc.id} className="p-4 bg-white border border-slate-200 rounded-xl shadow-xs flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-lg bg-teal-50 text-teal-700 flex items-center justify-center font-bold text-xs uppercase">
                      {doc.file_type}
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-slate-900">{doc.title}</h4>
                      <p className="text-[11px] text-slate-500">
                        Namespace: <code className="text-teal-700 font-mono font-semibold">{doc.namespace}</code> • {Math.round(doc.file_size_bytes / 1024)} KB
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                      Indexed
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
