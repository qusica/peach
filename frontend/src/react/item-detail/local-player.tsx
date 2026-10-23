import { useState } from 'react';
import { Button } from '@/components/base/buttons/button';
import { apiSend } from '../../api';

export function browserIsLocal(): boolean {
  const host = window.location.hostname.toLowerCase();
  return host === 'localhost' || host === '127.0.0.1' || host === '[::1]' || host === '::1';
}

/** A deliberate click opens the file on the SAME computer running Peach. */
export function LocalPlayerButton({ id }: { id: number }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  if (!browserIsLocal()) return null;
  const launch = async () => {
    if (busy) return;
    setBusy(true);
    setError('');
    try {
      await apiSend(`/api/open-local-player?id=${id}`, {}, 'POST');
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : '启动本机播放器失败');
    } finally {
      setBusy(false);
    }
  };
  return <div data-local-player="">
    <Button variant="secondary" disabled={busy} onClick={() => void launch()}>
      {busy ? '正在打开…' : '用本机默认播放器打开'}
    </Button>
    {error ? <span role="alert">{error}</span> : null}
  </div>;
}
