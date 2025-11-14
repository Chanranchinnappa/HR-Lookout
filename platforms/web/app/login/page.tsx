'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { authApi } from '@/lib/api';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const response = await authApi.login(username, password);
      console.log('Login successful:', response.data);

      // *** THE CRITICAL FIX: STORE TOKEN SO DASHBOARD WORKS ***
      if (response.data && response.data.token) {
        localStorage.setItem('token', response.data.token);
      } else {
        setError('No token returned from API.');
        setLoading(false);
        return;
      }

      // Redirect to home page
      router.push('/');
    } catch (err: any) {
      console.error('Login error:', err);
      setError(err.response?.data?.error || 'Invalid username or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50">
      <form 
        className="bg-white rounded-lg shadow p-8 max-w-md w-full"
        onSubmit={handleSubmit}
      >
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Sign in to your account</h2>
        {error && (
          <div className="bg-red-100 text-red-700 mb-4 px-4 py-2 rounded">{error}</div>
        )}
        <div className="mb-4">
          <label className="block mb-1 font-medium text-gray-700">Username</label>
          <input
            type="text"
            value={username}
            onChange={e => setUsername(e.target.value)}
            className="w-full border px-3 py-2 rounded"
            required
          />
        </div>
        <div className="mb-6">
          <label className="block mb-1 font-medium text-gray-700">Password</label>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            className="w-full border px-3 py-2 rounded"
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 rounded"
          disabled={loading}
        >
          {loading ? 'Signing in...' : 'Sign In'}
        </button>
      </form>
    </main>
  );
}
