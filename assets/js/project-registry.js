// Shared summaries; original case studies remain the authoritative long-form evidence.
export const projects = Object.freeze([
  {id:'transit', title:'Transit accessibility in DKI Jakarta', category:'Urban mobility', district:'jakarta', caseStudyUrl:'project-transit.html', landmarkId:'transit-station', availableInGame:true,
    shortDescription:'Who can reach essential facilities within a 60-minute transit budget?',
    methodology:'Network accessibility · AHP · Getis-Ord Gi*',
    finding:'Across 261 urban villages, the documented model reports a 26.6% average accessibility improvement with Mikrotrans. Gains remain geographically uneven.',
    caveat:'Modeled accessibility, not observed travel behaviour. The city below is conceptual geography.',
    scenarios:[{name:'A · Backbone network', score:29.67, text:'BRT, MRT, LRT and KRL without Mikrotrans feeders.'}, {name:'B · Mikrotrans integrated',score:37.55,text:'Full Jaklingko network, including 99 Mikrotrans JAK routes.'}],
    mapUrls:[{label:'Transit dashboard',url:'maps/transit_dashboard.html'}]},
  {id:'pangan',title:'Critical Roads for the Rice Supply Chain in West Java',category:'Food systems',district:'west-java',caseStudyUrl:'project-pangan.html',availableInGame:false,shortDescription:'Tracing the infrastructure supporting regional rice distribution.'},
  {id:'alphaearth-food',title:'Historical Paddy Screening in West Java',category:'Earth observation',district:'west-java',caseStudyUrl:'project-alphaearth-food.html',availableInGame:false,shortDescription:'Historical model-derived screening with explicit evidence boundaries.'},
  {id:'mbr',title:'A Satellite Proxy for Low-Income Communities in DKI Jakarta',category:'Urban morphology',district:'jakarta',caseStudyUrl:'project-mbr.html',landmarkId:'urban-neighbourhood',availableInGame:true,methodology:'Satellite embeddings · XGBoost · Temporal harmonization',finding:'The study models visible urban morphology as a proxy, complementary to official measures.',caveat:'This is not a household income estimate. The conceptual neighbourhood does not identify low-income residents or depict measured deprivation.',shortDescription:'A morphology-based proxy, complementary to official measures; not a household income estimate.'},
  {id:'cbd',title:'Mapping Indonesia’s Business Centers with DBSCAN',category:'Spatial clustering',district:'jakarta',caseStudyUrl:'project-cbd.html',landmarkId:'business-plaza',availableInGame:true,
    shortDescription:'Where do commercial centres emerge from 91,940 OpenStreetMap POIs?',methodology:'Adaptive DBSCAN · Haversine distance · OSM POI mining',
    finding:'Province-specific density thresholds group commercial POIs. The largest cluster is treated as the provincial CBD.',
    caveat:'A detected density cluster is not a municipal designation. OSM completeness and diffuse urban form limit the results.',
    mapUrls:[{label:'Jakarta interactive map',url:'maps/jakarta_map.html'},{label:'Indonesia interactive map',url:'maps/indonesia_map.html'}]},
  {id:'bandung-cafe',title:'Choosing where to visit: screening Bandung’s café neighbourhoods',category:'Site screening',district:'bandung',caseStudyUrl:'project-bandung-cafe.html',availableInGame:false,shortDescription:'Neighbourhood screening to guide site visits, with explicit limits on what the data can say.'}
].map(Object.freeze));
export const projectById = id => projects.find(project => project.id === id) || null;
