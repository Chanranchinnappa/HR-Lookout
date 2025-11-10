'use client';

import { useEffect, useState } from 'react';
import { employeesApi, organizationsApi } from '@/lib/api';
import type { Employee, Organization } from '@/types';

export default function EmployeesPage() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [selectedEmployee, setSelectedEmployee] = useState<Employee | null>(null);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  
  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  
  // Filters
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [organizationFilter, setOrganizationFilter] = useState('');
  const [jobTitleFilter, setJobTitleFilter] = useState('');
  
  // Form data
  const [formData, setFormData] = useState({
    employee_id: '',
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    job_title: '',
    hire_date: '',
    organization: '',
  });
  const [editingEmployee, setEditingEmployee] = useState<Employee | null>(null);

  useEffect(() => {
    fetchOrganizations();
  }, []);

  useEffect(() => {
    fetchEmployees();
  }, [currentPage, searchQuery, statusFilter, organizationFilter, jobTitleFilter]);

  const fetchOrganizations = async () => {
    try {
      const response = await organizationsApi.getAll();
      const data = response.data;
      // Handle both paginated and non-paginated responses
      if (data.results) {
        setOrganizations(data.results);
      } else if (Array.isArray(data)) {
        setOrganizations(data);
      } else {
        setOrganizations([]);
      }
    } catch (err: unknown) {
      console.error('Error fetching organizations:', err);
      setOrganizations([]);
    }
  };

  const fetchEmployees = async () => {
    try {
      setLoading(true);
      const params: any = { page: currentPage };
      if (statusFilter) params.employment_status = statusFilter;
      if (organizationFilter) params.organization = organizationFilter;
      if (jobTitleFilter) params.job_title = jobTitleFilter;
      if (searchQuery) params.search = searchQuery;

      const response = await employeesApi.getAll(params);
      const data = response.data;
      
      if (data.results) {
        setEmployees(data.results);
        setTotalCount(data.count);
        setTotalPages(Math.ceil(data.count / 10));
      } else {
        setEmployees(data);
      }
      setLoading(false);
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingEmployee) {
        await employeesApi.update(editingEmployee.id, formData);
        alert('Employee updated successfully!');
      } else {
        await employeesApi.create(formData);
        alert('Employee created successfully!');
      }
      setShowModal(false);
      setEditingEmployee(null);
      resetForm();
      fetchEmployees();
    } catch (err: any) {
      alert('Error: ' + (err.response?.data?.message || err.message));
    }
  };

  const handleEdit = (employee: Employee) => {
    setEditingEmployee(employee);
    setFormData({
      employee_id: employee.employee_id,
      first_name: employee.first_name,
      last_name: employee.last_name,
      email: employee.email,
      phone: employee.phone || '',
      job_title: employee.job_title,
      hire_date: employee.hire_date,
      organization: String(employee.organization),
    });
    setShowModal(true);
  };

  const handleDelete = async (id: number) => {
    if (confirm('Are you sure you want to delete this employee?')) {
      try {
        await employeesApi.delete(id);
        fetchEmployees();
      } catch (err: any) {
        alert('Error deleting employee');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      employee_id: '',
      first_name: '',
      last_name: '',
      email: '',
      phone: '',
      job_title: '',
      hire_date: '',
      organization: '',
    });
  };

  const viewDetails = (employee: Employee) => {
    setSelectedEmployee(employee);
    setShowDetailsModal(true);
  };

  if (loading && employees.length === 0) {
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
        <h1 className="text-4xl font-bold text-white drop-shadow-lg mb-2">Employees</h1>
        <p className="text-gray-300 text-lg">Manage your workforce</p>
      </div>

      {/* Search and Filters */}
      <div className="mb-6 space-y-4">
        <div className="flex gap-4 flex-wrap">
          <input
            type="text"
            placeholder="Search employees by name, email, or ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="flex-1 min-w-[250px] px-3 py-2.5 bg-slate-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
          />
          <button
            onClick={() => setShowModal(true)}
            className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-6 py-2.5 rounded-lg hover:from-blue-700 hover:to-blue-800 transition shadow-lg font-medium whitespace-nowrap"
          >
            + Add Employee
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1.5 text-gray-300">Status</label>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-full px-3 py-2.5 bg-slate-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            >
              <option value="">All Status</option>
              <option value="ACTIVE">Active</option>
              <option value="INACTIVE">Inactive</option>
              <option value="ON_LEAVE">On Leave</option>
              <option value="TERMINATED">Terminated</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1.5 text-gray-300">Organization</label>
            <select
              value={organizationFilter}
              onChange={(e) => setOrganizationFilter(e.target.value)}
              className="w-full px-3 py-2.5 bg-slate-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            >
              <option value="">All Organizations</option>
              {organizations.map((org) => (
                <option key={org.id} value={org.id}>
                  {org.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1.5 text-gray-300">Job Title</label>
            <select
              value={jobTitleFilter}
              onChange={(e) => setJobTitleFilter(e.target.value)}
              className="w-full px-3 py-2.5 bg-slate-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            >
              <option value="">All Roles</option>
              {[...new Set(employees.map(emp => emp.job_title))].sort().map((title) => (
                <option key={title} value={title}>
                  {title}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Employees Table */}
      {employees.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-300 text-xl mb-2">No employees</p>
          <p className="text-gray-400">Get started by creating a new employee.</p>
        </div>
      ) : (
        <>
          <div className="overflow-x-auto bg-slate-800/50 backdrop-blur-sm rounded-xl shadow-2xl border border-gray-700">
            <table className="min-w-full">
              <thead className="bg-slate-900/70">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-bold text-gray-300 uppercase tracking-wider">Employee</th>
                  <th className="px-6 py-4 text-left text-xs font-bold text-gray-300 uppercase tracking-wider">Email</th>
                  <th className="px-6 py-4 text-left text-xs font-bold text-gray-300 uppercase tracking-wider">Job Title</th>
                  <th className="px-6 py-4 text-left text-xs font-bold text-gray-300 uppercase tracking-wider">Organization</th>
                  <th className="px-6 py-4 text-left text-xs font-bold text-gray-300 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-4 text-left text-xs font-bold text-gray-300 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-700">
                {employees.map((employee) => (
                  <tr key={employee.id} className="hover:bg-slate-700/30 transition">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-10 w-10 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-white font-bold">
                          {employee.first_name[0]}{employee.last_name[0]}
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-semibold text-white">
                            {employee.first_name} {employee.last_name}
                          </div>
                          <div className="text-sm text-gray-400">{employee.employee_id}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{employee.email}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{employee.job_title}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                      {employee.organization_name || organizations.find(o => o.id === Number(employee.organization))?.name || `Org ${employee.organization}`}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                        employee.employment_status === 'ACTIVE'
                          ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                          : employee.employment_status === 'INACTIVE'
                          ? 'bg-gray-500/20 text-gray-400 border border-gray-500/30'
                          : employee.employment_status === 'ON_LEAVE'
                          ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
                          : 'bg-red-500/20 text-red-400 border border-red-500/30'
                      }`}>
                        {employee.employment_status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm space-x-3">
                      <button
                        onClick={() => viewDetails(employee)}
                        className="text-cyan-400 hover:text-cyan-300 font-medium transition"
                      >
                        Details
                      </button>
                      <button
                        onClick={() => handleEdit(employee)}
                        className="text-blue-400 hover:text-blue-300 font-medium transition"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(employee.id)}
                        className="text-red-400 hover:text-red-300 font-medium transition"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="mt-6 flex items-center justify-between">
            <p className="text-sm text-gray-300">
              Page {currentPage} of {totalPages} ({totalCount} employees)
            </p>
            <div className="flex gap-2">
              <button
                onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                disabled={currentPage === 1}
                className="px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-600 disabled:opacity-50 disabled:cursor-not-allowed transition font-medium"
              >
                Previous
              </button>
              <button
                onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                disabled={currentPage === totalPages}
                className="px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-600 disabled:opacity-50 disabled:cursor-not-allowed transition font-medium"
              >
                Next
              </button>
            </div>
          </div>
        </>
      )}

      {/* Floating Modal Form */}
      {showModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 w-full max-w-2xl max-h-[85vh] overflow-y-auto shadow-2xl border border-gray-700">
            <h2 className="text-3xl font-bold mb-6 text-white">
              {editingEmployee ? 'Edit Employee' : 'New Employee'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1.5 text-gray-300">Employee ID *</label>
                  <input
                    type="text"
                    required
                    value={formData.employee_id}
                    onChange={(e) => setFormData({ ...formData, employee_id: e.target.value })}
                    className="w-full px-3 py-2.5 bg-slate-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1.5 text-gray-300">Organization *</label>
                  <select
                    required
                    value={formData.organization}
                    onChange={(e) => setFormData({ ...formData, organization: e.target.value })}
                    className="w-full px-3 py-2.5 bg-slate-900 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  >
                    <option value="">Select Organization</option>
                    {organizations.map((org) => (
                      <option key={org.id} value={org.id}>
                        {org.name}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1.5 text-gray-300">First Name *</label>
                  <input
                    type="text"
                    required
                    value={formData.first_name}
                    onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                    className="w-full px-3 py-2.5 bg-slate-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1.5 text-gray-300">Last Name *</label>
                  <input
                    type="text"
                    required
                    value={formData.last_name}
                    onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                    className="w-full px-3 py-2.5 bg-slate-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1.5 text-gray-300">Email *</label>
                  <input
                    type="email"
                    required
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className="w-full px-3 py-2.5 bg-slate-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1.5 text-gray-300">Phone</label>
                  <input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    className="w-full px-3 py-2.5 bg-slate-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1.5 text-gray-300">Job Title *</label>
                  <input
                    type="text"
                    required
                    value={formData.job_title}
                    onChange={(e) => setFormData({ ...formData, job_title: e.target.value })}
                    className="w-full px-3 py-2.5 bg-slate-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1.5 text-gray-300">Hire Date *</label>
                  <input
                    type="date"
                    required
                    value={formData.hire_date}
                    onChange={(e) => setFormData({ ...formData, hire_date: e.target.value })}
                    className="w-full px-3 py-2.5 bg-slate-900 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
                  />
                </div>
              </div>
              <div className="flex gap-3 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-gradient-to-r from-blue-600 to-blue-700 text-white py-3 rounded-lg hover:from-blue-700 hover:to-blue-800 transition font-medium shadow-lg"
                >
                  {editingEmployee ? 'Update Employee' : 'Create Employee'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false);
                    setEditingEmployee(null);
                    resetForm();
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

      {/* Details Modal */}
      {showDetailsModal && selectedEmployee && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 w-full max-w-2xl max-h-[85vh] overflow-y-auto shadow-2xl border border-gray-700">
            <h2 className="text-3xl font-bold mb-6 text-white">Employee Details</h2>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-400">Employee ID</p>
                  <p className="text-white font-medium">{selectedEmployee.employee_id}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-400">Full Name</p>
                  <p className="text-white font-medium">{selectedEmployee.first_name} {selectedEmployee.last_name}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-400">Email</p>
                  <p className="text-white font-medium">{selectedEmployee.email}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-400">Phone</p>
                  <p className="text-white font-medium">{selectedEmployee.phone || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-400">Job Title</p>
                  <p className="text-white font-medium">{selectedEmployee.job_title}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-400">Status</p>
                  <p className="text-white font-medium">{selectedEmployee.employment_status}</p>
                </div>
              </div>
            </div>
            <div className="mt-6">
              <button
                onClick={() => setShowDetailsModal(false)}
                className="w-full bg-slate-700 text-white py-3 rounded-lg hover:bg-slate-600 transition font-medium"
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
