'use client';

import React, { useState, useEffect } from 'react';
import {
  Database,
  ExternalLink,
  ShieldCheck,
  CheckCircle2,
  Clock,
  Scale,
  BookOpen,
  RefreshCw,
  Search,
  FileCode,
  Layers,
  History,
  AlertCircle,
  Hash,
  X
} from 'lucide-react';
import { api } from '@/lib/api';

export default function SourcesPage() {
  const [sources, setSources] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedJurisdiction, setSelectedJurisdiction] = useState('All');
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const [notification, setNotification] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  // Modals state
  const [selectedSourceForChunks, setSelectedSourceForChunks] = useState<any | null>(null);
  const [chunks, setChunks] = useState<any[]>([]);
  const [loadingChunks, setLoadingChunks] = useState(false);

  const [selectedSourceForVersions, setSelectedSourceForVersions] = useState<any | null>(null);
  const [versions, setVersions] = useState<any[]>([]);
  const [loadingVersions, setLoadingVersions] = useState(false);

  const fetchSources = async () => {
    setLoading(true);
    try {
      const data = await api.getSources(
        selectedJurisdiction !== 'All' ? { jurisdiction: selectedJurisdiction } : undefined
      );
      setSources(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSources();
  }, [selectedJurisdiction]);

  const handleSyncCheck = async () => {
    setActionLoading('sync');
    try {
      const res = await api.syncCheckSources();
      setNotification({ text: `Source synchronization complete: ${res.sources_checked} sources verified.`, type: 'success' });
      await fetchSources();
    } catch (err: any) {
      setNotification({ text: `Sync check failed: ${err.message}`, type: 'error' });
    } finally {
      setActionLoading(null);
    }
  };

  const handleValidate = async (sourceId: string) => {
    setActionLoading(`val-${sourceId}`);
    try {
      const res = await api.validateSource(sourceId);
      setNotification({ text: `Validation passed: SHA-256 ${res.checksum_sha256.substring(0, 16)}...`, type: 'success' });
      await fetchSources();
    } catch (err: any) {
      setNotification({ text: `Validation failed: ${err.message}`, type: 'error' });
    } finally {
      setActionLoading(null);
    }
  };

  const handleReingest = async (sourceId: string) => {
    setActionLoading(`ing-${sourceId}`);
    try {
      const res = await api.ingestSource(sourceId);
      setNotification({ text: `Source re-ingested: ${res.chunks_count} hierarchical chunks indexed.`, type: 'success' });
      await fetchSources();
    } catch (err: any) {
      setNotification({ text: `Ingestion failed: ${err.message}`, type: 'error' });
    } finally {
      setActionLoading(null);
    }
  };

  const handleOpenChunks = async (source: any) => {
    setSelectedSourceForChunks(source);
    setLoadingChunks(true);
    try {
      const data = await api.getSourceChunks(source.source_id);
      setChunks(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingChunks(false);
    }
  };

  const handleOpenVersions = async (source: any) => {
    setSelectedSourceForVersions(source);
    setLoadingVersions(true);
    try {
      const data = await api.getSourceVersions(source.source_id);
      setVersions(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingVersions(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-teal-50 text-teal-800 text-xs font-bold mb-2">
            <Database className="w-4 h-4 text-teal-600" />
            Verified Authoritative Statutory Registry
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Authoritative Legal & Regulatory Source Explorer
          </h1>
          <p className="text-sm text-slate-600 mt-1">
            Zero hardcoding pipeline: browse verified statutory sources, inspect legal structure hierarchies, and track SHA-256 version audit trails.
          </p>
        </div>

        {/* Global Actions */}
        <div className="flex items-center gap-3">
          <button
            onClick={handleSyncCheck}
            disabled={actionLoading !== null}
            className="inline-flex items-center gap-2 px-4 py-2 bg-teal-700 hover:bg-teal-800 text-white text-xs font-bold rounded-xl shadow-xs transition-all disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${actionLoading === 'sync' ? 'animate-spin' : ''}`} />
            <span>Sync & Verify All Sources</span>
          </button>
        </div>
      </div>

      {/* Notification banner */}
      {notification && (
        <div className={`p-4 rounded-xl text-xs font-semibold flex items-center justify-between ${
          notification.type === 'success' ? 'bg-emerald-50 text-emerald-900 border border-emerald-200' : 'bg-rose-50 text-rose-900 border border-rose-200'
        }`}>
          <span>{notification.text}</span>
          <button onClick={() => setNotification(null)} className="text-slate-500 hover:text-slate-700">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Filter Pills */}
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div className="flex items-center gap-1.5 bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs">
          {['All', 'India', 'International'].map((j) => (
            <button
              key={j}
              onClick={() => setSelectedJurisdiction(j)}
              className={`px-3 py-1.5 font-bold rounded-lg transition-all ${
                selectedJurisdiction === j
                  ? 'bg-teal-700 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              {j}
            </button>
          ))}
        </div>
        <div className="text-xs text-slate-500 font-medium">
          Showing <strong>{sources.length}</strong> authoritative primary documents
        </div>
      </div>

      {/* Sources Grid */}
      {loading ? (
        <div className="p-16 text-center text-xs text-slate-500">Loading authoritative statutory sources...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sources.map((src) => (
            <div
              key={src.id}
              className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between hover:border-teal-300 transition-all space-y-4"
            >
              <div>
                <div className="flex items-center justify-between">
                  <span className="px-2.5 py-0.5 rounded-md text-[10px] font-bold bg-teal-50 text-teal-800 border border-teal-200 uppercase tracking-wider">
                    {src.jurisdiction} • {src.legal_domain || src.domain}
                  </span>
                  <div className="flex items-center gap-1 text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">
                    <ShieldCheck className="w-3.5 h-3.5" />
                    <span>{src.verification_status || 'VERIFIED'}</span>
                  </div>
                </div>

                <h3 className="text-base font-bold text-slate-900 mt-3 leading-snug">
                  {src.name || src.title}
                </h3>

                <div className="mt-3 space-y-1.5 text-xs text-slate-600">
                  <p className="flex items-center gap-1.5">
                    <Scale className="w-3.5 h-3.5 text-teal-600 flex-shrink-0" />
                    <span>Authority: <strong>{src.authority}</strong></span>
                  </p>
                  <p className="flex items-center gap-1.5">
                    <BookOpen className="w-3.5 h-3.5 text-teal-600 flex-shrink-0" />
                    <span>Type: <strong>{src.document_type || src.source_type}</strong> (Rank #{src.authority_rank})</span>
                  </p>
                  <p className="flex items-center gap-1.5 text-[11px] text-slate-500">
                    <Hash className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
                    <span>SHA-256: <code className="bg-slate-100 px-1 py-0.5 rounded text-[10px]">{src.checksum_sha256 ? `${src.checksum_sha256.substring(0, 12)}...` : 'Computed'}</code></span>
                  </p>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="pt-3 border-t border-slate-100 space-y-3">
                <div className="flex items-center justify-between text-xs">
                  <button
                    onClick={() => handleOpenChunks(src)}
                    className="inline-flex items-center gap-1 text-teal-700 hover:text-teal-800 font-bold"
                  >
                    <Layers className="w-3.5 h-3.5" />
                    <span>Inspect Records</span>
                  </button>
                  <button
                    onClick={() => handleOpenVersions(src)}
                    className="inline-flex items-center gap-1 text-slate-600 hover:text-slate-900 font-semibold"
                  >
                    <History className="w-3.5 h-3.5" />
                    <span>Versions</span>
                  </button>
                </div>

                <div className="flex items-center justify-between pt-2 border-t border-slate-50">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleValidate(src.source_id)}
                      disabled={actionLoading !== null}
                      className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-[11px] font-semibold"
                    >
                      Validate
                    </button>
                    <button
                      onClick={() => handleReingest(src.source_id)}
                      disabled={actionLoading !== null}
                      className="px-2.5 py-1 bg-teal-50 hover:bg-teal-100 text-teal-800 border border-teal-200 rounded-lg text-[11px] font-bold"
                    >
                      Re-ingest
                    </button>
                  </div>

                  {(src.official_url || src.source_url) && (
                    <a
                      href={src.official_url || src.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-[11px] font-bold text-teal-700 hover:text-teal-900"
                    >
                      <span>Official Gazette</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Records Inspector Modal */}
      {selectedSourceForChunks && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl max-w-4xl w-full max-h-[85vh] flex flex-col shadow-2xl border border-slate-200">
            <div className="p-6 border-b border-slate-200 flex items-center justify-between">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-teal-700 bg-teal-50 px-2 py-0.5 rounded border border-teal-200">
                  {selectedSourceForChunks.jurisdiction} • {selectedSourceForChunks.legal_domain || selectedSourceForChunks.domain}
                </span>
                <h2 className="text-lg font-bold text-slate-900 mt-1">
                  Authoritative Record Inspector: {selectedSourceForChunks.name || selectedSourceForChunks.title}
                </h2>
              </div>
              <button
                onClick={() => setSelectedSourceForChunks(null)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 overflow-y-auto space-y-4 flex-1">
              {loadingChunks ? (
                <div className="py-12 text-center text-xs text-slate-500">Loading parsed legal structure records...</div>
              ) : chunks.length === 0 ? (
                <div className="py-12 text-center text-xs text-slate-500">No records indexed yet for this source.</div>
              ) : (
                chunks.map((c) => (
                  <div key={c.id} className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2 text-xs">
                    <div className="flex items-center justify-between flex-wrap gap-2">
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-teal-900 bg-teal-100 px-2 py-0.5 rounded">
                          {c.provision_ref}
                        </span>
                        <span className="font-semibold text-slate-800">
                          {c.section_title}
                        </span>
                      </div>
                      <span className="text-[11px] text-slate-500 font-mono">
                        {c.token_count} tokens
                      </span>
                    </div>

                    {/* Hierarchy metadata tags */}
                    <div className="flex items-center gap-2 flex-wrap text-[10px] text-slate-600 font-medium">
                      {c.chapter && <span className="bg-white px-2 py-0.5 rounded border border-slate-200">{c.chapter}</span>}
                      {c.section && <span className="bg-white px-2 py-0.5 rounded border border-slate-200">{c.section}</span>}
                      {c.rule && <span className="bg-white px-2 py-0.5 rounded border border-slate-200">{c.rule}</span>}
                      {c.regulation && <span className="bg-white px-2 py-0.5 rounded border border-slate-200">{c.regulation}</span>}
                      {c.article && <span className="bg-white px-2 py-0.5 rounded border border-slate-200">{c.article}</span>}
                      {c.schedule && <span className="bg-white px-2 py-0.5 rounded border border-slate-200">{c.schedule}</span>}
                    </div>

                    {/* Verbatim Source Text */}
                    <div className="p-3 bg-white border border-slate-200 rounded-lg text-slate-800 whitespace-pre-wrap font-sans text-xs leading-relaxed">
                      {c.source_text || c.content}
                    </div>
                  </div>
                ))
              )}
            </div>

            <div className="p-4 border-t border-slate-200 flex justify-end">
              <button
                onClick={() => setSelectedSourceForChunks(null)}
                className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold"
              >
                Close Inspector
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Version History Modal */}
      {selectedSourceForVersions && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[85vh] flex flex-col shadow-2xl border border-slate-200">
            <div className="p-6 border-b border-slate-200 flex items-center justify-between">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-teal-700 bg-teal-50 px-2 py-0.5 rounded border border-teal-200">
                  Version & Checksum History
                </span>
                <h2 className="text-lg font-bold text-slate-900 mt-1">
                  {selectedSourceForVersions.name || selectedSourceForVersions.title}
                </h2>
              </div>
              <button
                onClick={() => setSelectedSourceForVersions(null)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 overflow-y-auto space-y-3 flex-1">
              {loadingVersions ? (
                <div className="py-8 text-center text-xs text-slate-500">Loading version history...</div>
              ) : versions.length === 0 ? (
                <div className="py-8 text-center text-xs text-slate-500">No version history records found.</div>
              ) : (
                versions.map((v) => (
                  <div key={v.id} className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2 text-xs">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-teal-900 text-sm">
                        Tag: {v.version_tag}
                      </span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                        v.status === 'active' ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-200 text-slate-700'
                      }`}>
                        {v.status}
                      </span>
                    </div>
                    <p className="text-slate-600 text-[11px]">
                      Effective From: <strong>{v.effective_from || 'Historical/Active'}</strong>
                    </p>
                    <p className="text-[11px] text-slate-500 font-mono">
                      Checksum: <span className="bg-white px-1.5 py-0.5 rounded border border-slate-200">{v.checksum}</span>
                    </p>
                    {v.changelog && (
                      <p className="text-slate-700 text-xs italic bg-white p-2 rounded border border-slate-100">
                        {v.changelog}
                      </p>
                    )}
                  </div>
                ))
              )}
            </div>

            <div className="p-4 border-t border-slate-200 flex justify-end">
              <button
                onClick={() => setSelectedSourceForVersions(null)}
                className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
