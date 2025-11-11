'use client';

import { useParams, useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';
import { employeesApi } from '@/lib/api';

export default function DepartmentEmployeesPage() {
  const { id } = useParams();
  const router = useRouter();
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const empRes = await employeesApi.getAll({ department: id });
        setEmployees(empRes.data.results || empRes.data || []);
      } catch (error) {
        console.error('Error fetching employees:', error);
      }
      setLoading(false);
    };
    fetchData();
  }, [id]);

  if (loading) return <div className="text-white p-10 text-xl">Loading...</div>;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <button
            onClick={() => router.back()}
            className="text-blue-400 hover:text-blue-300 text-sm flex items-center gap-2 mb-4"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back
          </button>
          <h1 className="text-3xl text-white font-bold mb-6">Department Employees</h1>
        </div>

        <h2 className="text-xl text-purple-300 font-semibold mb-3">Employees in Department</h2>
        <div className="space-y-4">
          {employees.length === 0 && (
            <div className="text-gray-400 text-center py-12 bg-slate-800/30 rounded-lg border border-gray-700">
              No employees in this department.
            </div>
          )}
          {employees.map((emp: any) => (
            <div key={emp.id} className="p-4 bg-slate-900 rounded-lg border border-slate-700 text-white hover:border-purple-500 transition">
              <div className="flex gap-4 items-center">
                <span className="w-12 h-12 bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center rounded-full font-bold text-lg shadow-lg">
                  {emp.first_name[0]}{emp.last_name[0]}
                </span>
                <div>
                  <div className="text-lg font-semibold">{emp.first_name} {emp.last_name}</div>
                  <div className="text-sm text-gray-400">{emp.email}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
