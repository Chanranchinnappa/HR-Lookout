//services/web/app/organizations/page.tsx

'use client';

import { useEffect, useState } from 'react';
import { organizationsApi } from '@/lib/api';
import { Organization } from '@/types';

export default function OrganizationsPage() {
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    legal_name: '',
    email: '',
    phone: '',
    website: '',
    address_line1: '',
    address_line2: '',
    city: '',
    state: '',
    postal_code: '',
    country: 'United States',
    tax_id: '',
    registration_number: '',
    fiscal_year_start: '',
    currency: 'USD',
    timezone: 'UTC',
  });
  const [editingOrg, setEditingOrg] = useState<Organization | null>(null);

  useEffect(() => {
    fetchOrganizations();
  }, []);

  const fetchOrganizations = async () => {
    try {
      const res = await organizationsApi.getAll();
      setOrganizations(res.data.results || res.data);
      setLoading(false);
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingOrg) {
        await organizationsApi.update(editingOrg.id, formData);
        alert('Organization updated!');
      } else {
        await organizationsApi.create(formData);
        alert('Organization created!');
      }
      setShowForm(false);
      setEditingOrg(null);
      setFormData({
        name: '',
        legal_name: '',
        email: '',
        phone: '',
        website: '',
        address_line1: '',
        address_line2: '',
        city: '',
        state: '',
        postal_code: '',
        country: 'United States',
        tax_id: '',
        registration_number: '',
        fiscal_year_start: '',
        currency: 'USD',
        timezone: 'UTC',
      });
      fetchOrganizations();
    } catch (err: any) {
      alert('Error: ' + (err.response?.data?.message || err.message));
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm('Are you sure you want to delete this organization?')) {
      try {
        await organizationsApi.delete(id);
        fetchOrganizations();
      } catch (err: any) {
        alert('Error deleting organization: ' + err.message);
      }
    }
  };

  const handleEdit = (org: Organization) => {
    setEditingOrg(org);
    setShowForm(true);
    setFormData({
      name: org.name,
      legal_name: org.legal_name,
      email: org.email,
      phone: org.phone || '',
      website: org.website || '',
      address_line1: org.address_line1,
      address_line2: org.address_line2 || '',
      city: org.city,
      state: org.state,
      postal_code: org.postal_code,
      country: org.country,
      tax_id: org.tax_id,
      registration_number: org.registration_number || '',
      fiscal_year_start: org.fiscal_year_start,
      currency: org.currency,
      timezone: org.timezone,
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-red-400 text-xl">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-4xl font-bold text-white drop-shadow-lg mb-2">Organizations</h1>
        <p className="text-gray-300 text-lg">Manage your organizations</p>
      </div>

      <div className="flex justify-end mb-6">
        <button
          onClick={() => {
            if (showForm) {
              setShowForm(false);
              setEditingOrg(null);
              setFormData({
                name: '',
                legal_name: '',
                email: '',
                phone: '',
                website: '',
                address_line1: '',
                address_line2: '',
                city: '',
                state: '',
                postal_code: '',
                country: 'United States',
                tax_id: '',
                registration_number: '',
                fiscal_year_start: '',
                currency: 'USD',
                timezone: 'UTC',
              });
            } else {
              setShowForm(true);
            }
          }}
          className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-6 py-3 rounded-lg hover:from-blue-700 hover:to-blue-800 transition shadow-lg font-medium"
        >
          {showForm ? 'Cancel' : '+ Add Organization'}
        </button>
      </div>

      {/* Organizations Grid */}
      {organizations.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-300 text-xl mb-2">No organizations</p>
          <p className="text-gray-400">Get started by creating a new organization.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {organizations.map((org) => (
            <div
              key={org.id}
              className="bg-slate-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-6 shadow-xl hover:shadow-2xl transition"
            >
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-bold text-white">{org.name}</h3>
                <span
                  className={`px-3 py-1 rounded-full text-xs font-bold ${
                    org.is_active
                      ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                      : 'bg-gray-500/20 text-gray-400 border border-gray-500/30'
                  }`}
                >
                  {org.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
              <div className="space-y-2 mb-4">
                <p className="text-gray-300 text-sm">
                  <span className="font-medium">Email:</span> {org.email}
                </p>
                <p className="text-gray-300 text-sm">
                  <span className="font-medium">Tax ID:</span> {org.tax_id}
                </p>
                <p className="text-gray-300 text-sm">
                  <span className="font-medium">Location:</span> {org.city}, {org.state}
                </p>
                {org.employee_count !== undefined && (
                  <p className="text-gray-300 text-sm">
                    <span className="font-medium">Employees:</span> {org.employee_count}
                  </p>
                )}
              </div>
              <div className="flex gap-3 pt-3 border-t border-gray-700">
                <button
                  onClick={() => handleEdit(org)}
                  className="text-blue-400 hover:text-blue-300 text-sm font-medium transition"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(org.id)}
                  className="text-red-400 hover:text-red-300 text-sm font-medium transition"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Floating Modal Form */}
      {showForm && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 w-full max-w-3xl max-h-[85vh] overflow-y-auto shadow-2xl border border-gray-700">
            <h2 className="text-3xl font-bold mb-6 text-white">
              {editingOrg ? 'Edit Organization' : 'New Organization'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-300">Organization Name *</label>
                  <input
                    type="text"
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full px-3 py-2.5 bg-slate-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-300">Legal Name *</label>
                  <input
                    type="text"
                    required
                    value={formData.legal_name}
                    onChange={(e) => setFormData({ ...formData, legal_name: e.target.value })}
                    className="w-full px-3 py-2.5 bg-slate-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-300">Email *</label>
                  <input
                    type="email"
                    required
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className="w-full px-3 py-2.5 bg-slate-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-300">Phone</label>
                  <input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    className="w-full px-3 py-2.5 bg-slate-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium mb-2 text-gray-300">Address Line 1 *</label>
                  <input
                    type="text"
                    required
                    value={formData.address_line1}
                    onChange={(e) => setFormData({ ...formData, address_line1: e.target.value })}
                    className="w-full px-3 py-2.5 bg-slate-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-300">City *</label>
                  <input
                    type="text"
                    required
                    value={formData.city}
                    onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                    className="w-full px-3 py-2.5 bg-slate-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-300">State *</label>
                  <input
                    type="text"
                    required
                    value={formData.state}
                    onChange={(e) => setFormData({ ...formData, state: e.target.value })}
                    className="w-full px-3 py-2.5 bg-slate-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-300">Postal Code *</label>
                  <input
                    type="text"
                    required
                    value={formData.postal_code}
                    onChange={(e) => setFormData({ ...formData, postal_code: e.target.value })}
                    className="w-full px-3 py-2.5 bg-slate-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-300">Tax ID *</label>
                  <input
                    type="text"
                    required
                    value={formData.tax_id}
                    onChange={(e) => setFormData({ ...formData, tax_id: e.target.value })}
                    className="w-full px-3 py-2.5 bg-slate-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium mb-2 text-gray-300">Fiscal Year Start *</label>
                  <input
                    type="date"
                    required
                    value={formData.fiscal_year_start}
                    onChange={(e) => setFormData({ ...formData, fiscal_year_start: e.target.value })}
                    className="w-full px-3 py-2.5 bg-slate-900 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  />
                </div>
              </div>
              <div className="flex gap-3 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-gradient-to-r from-blue-600 to-blue-700 text-white py-3 rounded-lg hover:from-blue-700 hover:to-blue-800 transition font-medium shadow-lg"
                >
                  {editingOrg ? 'Update Organization' : 'Create Organization'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowForm(false);
                    setEditingOrg(null);
                  }}
                  className="flex-1 bg-slate-700 text-white py-3 rounded-lg hover:bg-slate-600 transition font-medium"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
