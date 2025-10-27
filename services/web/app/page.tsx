'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { organizationsApi, employeesApi } from '@/lib/api';

export default function Home() {
  const [stats, setStats] = useState({
    organizations: 0,
    employees: 0,
    systemStatus: 'All Systems Operational',
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const [orgsRes, empsRes] = await Promise.all([
        organizationsApi.getAll(),
        employeesApi.getAll(),
      ]);
      
      const orgsData = orgsRes.data.results || orgsRes.data || [];
      const empsData = empsRes.data.results || empsRes.data || [];
      
      setStats({
        organizations: Array.isArray(orgsData) ? orgsData.length : 0,
        employees: Array.isArray(empsData) ? empsData.length : 0,
        systemStatus: 'All Systems Operational',
      });
      setLoading(false);
    } catch (error) {
      console.error('Error fetching stats:', error);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white drop-shadow-lg mb-2">Dashboard</h1>
        <p className="text-gray-300 text-lg">Welcome to HR-Lookout</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {/* Organizations Card */}
        <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 shadow-xl border border-gray-700 hover:shadow-2xl transition">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-blue-500/20 rounded-lg">
              <svg className="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
          </div>
          <h3 className="text-gray-400 text-sm font-medium mb-1">Organizations</h3>
          <p className="text-4xl font-bold text-white mb-4">{loading ? '...' : stats.organizations}</p>
          <Link
            href="/organizations"
            className="text-blue-400 hover:text-blue-300 text-sm font-medium transition flex items-center"
          >
            View all →
          </Link>
        </div>

        {/* Employees Card */}
        <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 shadow-xl border border-gray-700 hover:shadow-2xl transition">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-cyan-500/20 rounded-lg">
              <svg className="w-8 h-8 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
          </div>
          <h3 className="text-gray-400 text-sm font-medium mb-1">Employees</h3>
          <p className="text-4xl font-bold text-white mb-4">{loading ? '...' : stats.employees}</p>
          <Link
            href="/employees"
            className="text-cyan-400 hover:text-cyan-300 text-sm font-medium transition flex items-center"
          >
            View all →
          </Link>
        </div>

        {/* System Status Card */}
        <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 shadow-xl border border-gray-700 hover:shadow-2xl transition">
          <div className="flex items-center justify-between mb-4">
            <div className="p-3 bg-green-500/20 rounded-lg">
              <svg className="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <h3 className="text-gray-400 text-sm font-medium mb-1">System Status</h3>
          <p className="text-lg font-bold text-green-400 mb-4">{stats.systemStatus}</p>
          <p className="text-gray-400 text-sm">
            Last checked: {new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}
          </p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-white mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link
            href="/employees"
            className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 shadow-xl border border-gray-700 hover:shadow-2xl hover:border-blue-500/50 transition group"
          >
            <h3 className="text-xl font-bold text-white mb-2 group-hover:text-blue-400 transition">Add Employee</h3>
            <p className="text-gray-400">Create new employee record</p>
          </Link>

          <Link
            href="/organizations"
            className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-xl p-6 shadow-xl border border-gray-700 hover:shadow-2xl hover:border-cyan-500/50 transition group"
          >
            <h3 className="text-xl font-bold text-white mb-2 group-hover:text-cyan-400 transition">Add Organization</h3>
            <p className="text-gray-400">Register new organization</p>
          </Link>
        </div>
      </div>
    </div>
  );
}
