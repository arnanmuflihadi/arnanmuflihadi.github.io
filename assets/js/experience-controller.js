// One entry across the multipage portfolio. Home and Work own the shared living scene.
import{projects}from'./project-registry.js?v=22';
const integrated=['','index.html','portfolio.html'].includes(location.pathname.split('/').pop());
if(integrated){import('./living-atlas-controller.js?v=f1').then(({bootLivingAtlas})=>bootLivingAtlas());}
else{
  const current=projects.find(p=>location.pathname.endsWith('/'+p.caseStudyUrl));
  const link=document.createElement('a');link.className='atlas-mode-switch';link.href=`index.html?${current?'project='+current.id:''}`;link.textContent='Living atlas';
  const nav=document.querySelector('[data-site-nav]');if(nav)nav.insertBefore(link,nav.querySelector('[data-theme-toggle]'));
}
