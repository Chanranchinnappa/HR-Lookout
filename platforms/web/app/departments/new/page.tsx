'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { departmentsApi, organizationsApi, employeesApi } from '@/lib/api';

export default function NewDepartmentPage() {
  const router = useRouter();
  const [organizations, setOrganizations] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [filteredEmployees, setFilteredEmployees] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    code: '',
    description: '',
    organization: '',
    head: '',
    is_active: true,
  });
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    if (formData.organization) {
      setFilteredEmployees(employees.filter(
        (emp: any) => emp.organization === parseInt(formData.organization)
      ));
    } else {
      setFilteredEmployees([]);
    }
  }, [formData.organization, employees]);

  const fetchData = async () => {
    try {
      const [orgsRes, empsRes] = await Promise.all([
        organizationsApi.getAll(),
        employeesApi.getAll(),
      ]);
      setOrganizations(orgsRes.data.results || orgsRes.data || []);
      setEmployees(empsRes.data.results || empsRes.data || []);
      setLoading(false);
    } catch (err) {
      setLoading(false);
      alert('Failed to load data');
      router.push('/departments');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await departmentsApi.create({
        ...formData,
        organization: parseInt(formData.organization),
        head: formData.head ? parseInt(formData.head) : null,
      });
      alert('Created!');
      router.push('/departments');
    } catch (err) {
      alert('Failed to create department');
      setSaving(false);
    }
  };

  if (loading) return <div className="p-8 text-lg text-center text-white">Loading...</div>;

  return (
    <div className="min-h-screen p-6 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <div className="max-w-3xl mx-auto">
        <h2 className="text-3xl font-bold mb-6 text-white">Add Department</h2>
        <form onSubmit={handleSubmit} className="space-y-6 bg-slate-900 p-8 rounded-2xl border border-gray-700 shadow-lg">
          <div>
            <label className="block text-sm font-medium mb-2 text-gray-300">Organization *</label>
            <select
              required
              value={formData.organization}
              onChange={e => setFormData({ ...formData, organization: e.target.value, head: '' })}
              className="w-full px-4 py-3 bg-slate-900 border border-gray-700 rounded-lg text-white"
            >
              <option value="">Select Organization</option>
              {organizations.map((org: any) => (
                <option key={org.id} value={org.id}>{org.name}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2 text-gray-300">Department Name *</label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={e => setFormData({ ...formData, name: e.target.value })}
              className="w-full px-4 py-3 bg-slate-900 border border-gray-700 rounded-lg text-white"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2 text-gray-300">Department Code *</label>
            <input
              required
              value={formData.code}
              onChange={e => setFormData({ ...formData, code: e.target.value })}
              className="w-full px-4 py-3 bg-slate-900 border border-gray-700 rounded-lg text-white"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2 text-gray-300">Description</label>
            <textarea
              value={formData.description}
              onChange={e => setFormData({ ...formData, description: e.target.value })}
              className="w-full px-4 py-3 bg-slate-900 border border-gray-700 rounded-lg text-white"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2 text-gray-300">Department Head</label>
            <select
              value={formData.head}
              onChange={e => setFormData({ ...formData, head: e.target.value })}
              className="w-full px-4 py-3 bg-slate-900 border border-gray-700 rounded-lg text-white"
            >
              <option value="">Select Head (optional)</option>
              {filteredEmployees.map((emp: any) => (
                <option key={emp.id} value={emp.id}>{emp.first_name} {emp.last_name}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2 text-gray-300">Status</label>
            <select
              value={formData.is_active ? 'true' : 'false'}
              onChange={e => setFormData({ ...formData, is_active: e.target.value === 'true' })}
              className="w-full px-4 py-3 bg-slate-900 border border-gray-700 rounded-lg text-white"
            >
              <option value="true">Active</option>
              <option value="false">Inactive</option>
            </select>
          </div>
          <div className="flex gap-4 pt-6 border-t border-gray-800">
            <button type="button" onClick={() => router.back()} className="flex-1 bg-slate-800 text-white py-3 rounded-lg hover:bg-slate-700">Cancel</button>
            <button type="submit" disabled={saving} className="flex-1 bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 disabled:opacity-50">{saving ? 'Saving...' : 'Create Department'}</button>
          </div>
        </form>
      </div>
    </div>
  );
}
