'use client';

import React, { useState, useEffect } from 'react';
import { Package, Plus, Trash2, Leaf, Globe, FileText, CheckCircle2, Layers } from 'lucide-react';
import { api } from '@/lib/api';

export default function ProductsPage() {
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  const [name, setName] = useState('');
  const [productType, setProductType] = useState('classical_ayurvedic');
  const [dosageForm, setDosageForm] = useState('Vati / Tablet');
  const [description, setDescription] = useState('');
  const [ingredientsText, setIngredientsText] = useState('Ashwagandha, Curcuma longa');
  const [claims, setClaims] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const data = await api.getProducts();
      setProducts(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleCreateProduct = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      const ings = ingredientsText.split(',').map((s) => ({
        common_name: s.trim(),
        is_biological_resource: true,
        source_origin_state: 'India'
      })).filter((i) => i.common_name);

      await api.createProduct({
        name,
        product_type: productType,
        dosage_form: dosageForm,
        description,
        intended_therapeutic_claims: claims,
        ingredients: ings
      });

      setShowModal(false);
      setName('');
      setDescription('');
      setClaims('');
      fetchProducts();
    } catch (err) {
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDeleteProduct = async (id: string) => {
    if (!confirm('Are you sure you want to delete this product workspace?')) return;
    try {
      await api.deleteProduct(id);
      fetchProducts();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-teal-50 text-teal-800 text-xs font-bold mb-2">
            <Package className="w-4 h-4 text-teal-600" />
            Enterprise Innovation Workspace
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Product Formulation Portfolio
          </h1>
          <p className="text-sm text-slate-600 mt-1">
            Manage formulations, ingredient provenance, target export jurisdictions, and regulatory dossiers in unified workspace.
          </p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2.5 bg-teal-700 hover:bg-teal-800 text-white text-xs font-semibold rounded-xl flex items-center gap-2 shadow-sm transition-all"
        >
          <Plus className="w-4 h-4" />
          <span>New Product Formulation</span>
        </button>
      </div>

      {/* Product List */}
      {loading ? (
        <div className="p-12 text-center text-xs text-slate-500">Loading products...</div>
      ) : products.length === 0 ? (
        <div className="p-12 bg-white border border-slate-200 rounded-2xl text-center space-y-3">
          <Package className="w-12 h-12 text-slate-300 mx-auto" />
          <h3 className="text-base font-bold text-slate-800">No Product Formulations Yet</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            Create your first formulation profile to generate complete IP landscapes, ABS compliance checks, and regulatory dossiers.
          </p>
          <button
            onClick={() => setShowModal(true)}
            className="px-4 py-2 bg-teal-700 text-white text-xs font-semibold rounded-lg"
          >
            Create Product Profile
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((prod) => (
            <div key={prod.id} className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between">
                  <span className="px-2.5 py-0.5 rounded-md text-[11px] font-bold bg-teal-50 text-teal-800 border border-teal-200 uppercase">
                    {prod.product_type.replace('_', ' ')}
                  </span>
                  <button
                    onClick={() => handleDeleteProduct(prod.id)}
                    className="text-slate-400 hover:text-rose-600 transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>

                <h3 className="text-base font-bold text-slate-900 mt-2">{prod.name}</h3>
                <p className="text-xs text-slate-600 line-clamp-2 mt-1">{prod.description || 'No description provided.'}</p>

                <div className="mt-4 pt-3 border-t border-slate-100 space-y-2 text-xs">
                  <div className="flex items-center gap-1.5 text-slate-700">
                    <Layers className="w-3.5 h-3.5 text-teal-600" />
                    <span>Dosage Form: <strong>{prod.dosage_form}</strong></span>
                  </div>

                  <div className="flex items-start gap-1.5 text-slate-700">
                    <Leaf className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0 mt-0.5" />
                    <span>
                      Ingredients: {prod.ingredients?.map((i: any) => i.common_name).join(', ') || 'None specified'}
                    </span>
                  </div>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
                <span>Created {new Date(prod.created_at).toLocaleDateString()}</span>
                <span className="font-semibold text-teal-700">Ready for Dossier</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4">
          <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 max-w-lg w-full p-6 space-y-4">
            <h2 className="text-lg font-bold text-slate-900">Create New Formulation Workspace</h2>

            <form onSubmit={handleCreateProduct} className="space-y-4 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Product Formulation Name</label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="e.g. Saptamrit Loha Extract Capsule"
                  required
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-600 focus:outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Category Type</label>
                  <select
                    value={productType}
                    onChange={(e) => setProductType(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg bg-white focus:outline-none"
                  >
                    <option value="classical_ayurvedic">Classical Ayurvedic (First Schedule)</option>
                    <option value="proprietary_ayurvedic">Patent or Proprietary (Rule 158B)</option>
                    <option value="ayurveda_aahar">Ayurveda Aahar (FSSAI 2022)</option>
                    <option value="phytopharmaceutical">Phytopharmaceutical Drug</option>
                    <option value="cosmetic">Herbal / Ayurvedic Cosmetic</option>
                  </select>
                </div>

                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Dosage Delivery Form</label>
                  <input
                    type="text"
                    value={dosageForm}
                    onChange={(e) => setDosageForm(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Botanical Ingredients (Comma separated)</label>
                <textarea
                  rows={2}
                  value={ingredientsText}
                  onChange={(e) => setIngredientsText(e.target.value)}
                  required
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Therapeutic / Wellness Claims</label>
                <textarea
                  rows={2}
                  value={claims}
                  onChange={(e) => setClaims(e.target.value)}
                  placeholder="Intended physiological indications..."
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 font-semibold text-slate-600 hover:bg-slate-100 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="px-5 py-2 bg-teal-700 hover:bg-teal-800 text-white font-semibold rounded-lg shadow-sm"
                >
                  {isSubmitting ? 'Saving...' : 'Save Product Profile'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
