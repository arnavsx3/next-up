import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '30s', target: 25 },
    { duration: '1m', target: 50 },
    { duration: '30s', target: 0 },
  ],
};

export default function () {
  const frontend = http.get('http://localhost/');
  check(frontend, {
    'frontend is 200': (r) => r.status === 200,
  });

  const backend = http.get('http://localhost/api/health');
  check(backend, {
    'backend is healthy': (r) => r.status === 200,
  });

  sleep(1);
}