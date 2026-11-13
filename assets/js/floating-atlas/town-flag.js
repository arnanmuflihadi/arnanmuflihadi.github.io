// Local review only. Public origins cannot opt into this unfinished vertical slice.
export function townDevelopmentEnabled(url=globalThis.location?.href){
 const u=new URL(url);return ['localhost','127.0.0.1','[::1]'].includes(u.hostname)&&u.searchParams.get('dev-town')==='s2f';
}
