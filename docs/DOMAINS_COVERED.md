# Active Scraper Sources

This list is generated from backend/app/scrapers/manifest.json and reflects the recorded local validation log from 2026-10-23.

**Selection rule:** a company is listed only when the log recorded PASS with at least one valid job record. Empty results, failures, timeouts, and companies absent from the log are excluded from the active manifest. A timeout can mean the scraper is slow or blocked rather than that the site has no jobs; excluded sources should be repaired and re-tested individually before being re-added.

- Active sources: **152**
- Tested manifest entries in the log: **491**
- PASS: **152**
- Excluded as EMPTY: **221**
- Excluded as FAIL: **8**
- Excluded as TIMEOUT: **110**
- Not present in the log: **10**

| Company | Official careers URL | Module |
|---|---|---|
| Meta | https://www.metacareers.com/ | metacareers_com.py |
| Netflix | https://jobs.netflix.com/ | netflix_com.py |
| OpenAI | https://openai.com/careers/ | openai_com.py |
| Anthropic | https://www.anthropic.com/careers | anthropic_com.py |
| xAI | https://x.ai/careers | x_ai.py |
| ByteDance | https://bytedance.com/careers | bytedance_com.py |
| TikTok | https://tiktok.com/careers | tiktok_com.py |
| Tencent | https://tencent.com/careers | tencent_com.py |
| Alibaba | https://alibaba.com/careers | alibaba_com.py |
| Huawei | https://huawei.com/careers | huawei_com.py |
| Samsung Electronics | https://samsung.com/careers | samsung_com.py |
| Sony | https://sony.com/careers | sony_com.py |
| Panasonic | https://panasonic.com/careers | panasonic_com.py |
| LG Electronics | https://lg.com/careers | lg_com.py |
| IBM | https://ibm.com/careers | ibm_com.py |
| Oracle | https://careers.oracle.com/ | oracle_com.py |
| Salesforce | https://careers.salesforce.com/ | salesforce_com.py |
| Adobe | https://careers.adobe.com/ | adobe_com.py |
| Cisco | https://jobs.cisco.com/ | cisco_com.py |
| Intel | https://intel.com/careers | intel_com.py |
| AMD | https://amd.com/careers | amd_com.py |
| Qualcomm | https://qualcomm.com/careers | qualcomm_com.py |
| Dell Technologies | https://dell.com/careers | dell_com.py |
| HP | https://hp.com/careers | hp_com.py |
| HPE | https://hpe.com/careers | hpe_com.py |
| Lenovo | https://lenovo.com/careers | lenovo_com.py |
| Broadcom | https://broadcom.com/careers | broadcom_com.py |
| Micron | https://micron.com/careers | micron_com.py |
| Texas Instruments | https://ti.com/careers | ti_com.py |
| Applied Materials | https://appliedmaterials.com/careers | appliedmaterials_com.py |
| ASML | https://asml.com/careers | asml_com.py |
| TSMC | https://tsmc.com/careers | tsmc_com.py |
| Synopsys | https://synopsys.com/careers | synopsys_com.py |
| Cadence Design Systems | https://cadence.com/careers | cadence_com.py |
| Ericsson | https://ericsson.com/careers | ericsson_com.py |
| Nokia | https://nokia.com/careers | nokia_com.py |
| Arista Networks | https://arista.com/careers | arista_com.py |
| Red Hat | https://redhat.com/careers | redhat_com.py |
| Canonical | https://canonical.com/careers | canonical_com.py |
| Databricks | https://databricks.com/careers | databricks_com.py |
| Snowflake | https://snowflake.com/careers | snowflake_com.py |
| Scale AI | https://scale.com/careers | scale_com.py |
| Cohere | https://cohere.com/careers | cohere_com.py |
| Mistral AI | https://mistral.ai/careers | mistral_ai.py |
| Hugging Face | https://huggingface.co/careers | huggingface_co.py |
| Perplexity | https://perplexity.ai/careers | perplexity_ai.py |
| Runway | https://runwayml.com/careers | runwayml_com.py |
| Stability AI | https://stability.ai/careers | stability_ai.py |
| ElevenLabs | https://elevenlabs.io/careers | elevenlabs_io.py |
| Character.AI | https://character.ai/careers | character_ai.py |
| Waymo | https://waymo.com/careers | waymo_com.py |
| Anduril | https://anduril.com/careers | anduril_com.py |
| MongoDB | https://mongodb.com/careers | mongodb_com.py |
| Redis | https://redis.io/careers | redis_io.py |
| Cockroach Labs | https://cockroachlabs.com/careers | cockroachlabs_com.py |
| Neo4j | https://neo4j.com/careers | neo4j_com.py |
| PlanetScale | https://planetscale.com/careers | planetscale_com.py |
| Supabase | https://supabase.com/careers | supabase_com.py |
| Vercel | https://vercel.com/careers | vercel_com.py |
| Netlify | https://netlify.com/careers | netlify_com.py |
| Fastly | https://fastly.com/careers | fastly_com.py |
| GitHub | https://github.careers/ | github_com.py |
| GitLab | https://about.gitlab.com/jobs/ | gitlab_com.py |
| Postman | https://postman.com/careers | postman_com.py |
| Figma | https://figma.com/careers | figma_com.py |
| Canva | https://canva.com/careers | canva_com.py |
| Notion | https://notion.com/careers | notion_com.py |
| Linear | https://linear.app/careers | linear_app.py |
| Airtable | https://airtable.com/careers | airtable_com.py |
| Asana | https://asana.com/careers | asana_com.py |
| Zapier | https://zapier.com/careers | zapier_com.py |
| 1Password | https://1password.com/careers | 1password_com.py |
| Grafana Labs | https://grafana.com/careers | grafana_com.py |
| New Relic | https://newrelic.com/careers | newrelic_com.py |
| JFrog | https://jfrog.com/careers | jfrog_com.py |
| CircleCI | https://circleci.com/careers | circleci_com.py |
| LaunchDarkly | https://launchdarkly.com/careers | launchdarkly_com.py |
| Amplitude | https://amplitude.com/careers | amplitude_com.py |
| Mixpanel | https://mixpanel.com/careers | mixpanel_com.py |
| Algolia | https://algolia.com/careers | algolia_com.py |
| Stripe | https://stripe.com/jobs | stripe_com.py |
| Checkout.com | https://checkout.com/careers | checkout_com.py |
| Ramp | https://ramp.com/careers | ramp_com.py |
| Monzo | https://monzo.com/careers | monzo_com.py |
| LTIMindtree | https://ltimindtree.com/careers | ltimindtree_com.py |
| Thoughtworks | https://thoughtworks.com/careers | thoughtworks_com.py |
| Kyndryl | https://kyndryl.com/careers | kyndryl_com.py |
| Deloitte | https://deloitte.com/careers | deloitte_com.py |
| Freshworks | https://www.freshworks.com/company/careers/ | freshworks_com.py |
| BrowserStack | https://www.browserstack.com/careers | browserstack_com.py |
| Chargebee | https://chargebee.com/careers | chargebee_com.py |
| Druva | https://druva.com/careers | druva_com.py |
| Glance | https://glance.com/careers | glance_com.py |
| Razorpay | https://razorpay.com/jobs/ | razorpay_com.py |
| Paytm | https://paytm.com/careers | paytm_com.py |
| CRED | https://careers.cred.club/ | cred_club.py |
| Slice | https://sliceit.com/careers | sliceit_com.py |
| Observe.AI | https://observe.ai/careers | observe_ai.py |
| Sarvam AI | https://www.sarvam.ai/careers | sarvam_ai.py |
| Fractal | https://fractal.ai/careers | fractal_ai.py |
| Mindtickle | https://mindtickle.com/careers | mindtickle_com.py |
| MoEngage | https://moengage.com/careers | moengage_com.py |
| Uniphore | https://uniphore.com/careers | uniphore_com.py |
| Airbnb | https://careers.airbnb.com/ | airbnb_com.py |
| Lyft | https://lyft.com/careers | lyft_com.py |
| Etsy | https://etsy.com/careers | etsy_com.py |
| Expedia Group | https://expediagroup.com/careers | expediagroup_com.py |
| Valve | https://valvesoftware.com/careers | valvesoftware_com.py |
| Intercom | https://intercom.com/careers | intercom_com.py |
| Zendesk | https://zendesk.com/careers | zendesk_com.py |
| CrowdStrike | https://crowdstrike.com/careers | crowdstrike_com.py |
| OVHcloud | https://careers.ovhcloud.com/en-in/ | ovhcloud_com.py |
| Scaleway | https://scaleway.com/careers | scaleway_com.py |
| Sentry | https://sentry.io/careers | sentry_io.py |
| Sourcegraph | https://sourcegraph.com/careers | sourcegraph_com.py |
| Replit | https://replit.com/careers | replit_com.py |
| Coursera | https://coursera.org/careers | coursera_org.py |
| Remote | https://remote.com/careers | remote_com.py |
| Wells Fargo | https://wellsfargo.com/careers | wellsfargo_com.py |
| HSBC | https://hsbc.com/careers | hsbc_com.py |
| Bosch | https://jobs.bosch.com | bosch_com.py |
| Toyota | https://toyota.com/careers | toyota_com.py |
| Northrop Grumman | https://jobs.northropgrumman.com/careers?start=0&pid=1340074844495&sort_by=timestamp | northropgrumman_com.py |
| Siemens Healthineers | https://siemens-healthineers.com/careers | siemens_healthineers_com.py |
| Illumina | https://illumina.com/careers | illumina_com.py |
| Moderna | https://modernatx.com/careers | modernatx_com.py |
| Sanofi | https://sanofi.com/careers | sanofi_com.py |
| Eli Lilly | https://careers.lilly.com/us/en/search-results | lilly_com.py |
| Tempus AI | https://tempus.wd5.myworkdayjobs.com/Tempus_Careers | tempus_com.py |
| L'Oréal | https://loreal.com/careers | loreal_com.py |
| Unilever | https://careers.unilever.com/en/search-jobs | unilever_com.py |
| Coca-Cola | https://coke.wd1.myworkdayjobs.com/coca-cola-careers | coca_colacompany_com.py |
| Nike | https://nike.com/careers | nike_com.py |
| Flexport | https://flexport.com/careers | flexport_com.py |
| Samsara | https://samsara.com/careers | samsara_com.py |
| Dassault Systèmes | https://3ds.com/careers | 3ds_com.py |
| PTC | https://ptc.com/careers | ptc_com.py |
| Bentley Systems | https://bentley.com/careers | bentley_com.py |
| Rakuten | https://rakuten.com/careers | rakuten_com.py |
| Mercari | https://careers.mercari.com/ | mercari_com.py |
| Telstra | https://telstra.com.au/careers | telstra_com_au.py |
| Trend Micro | https://trendmicro.com/careers | trendmicro_com.py |
| Darktrace | https://darktrace.com/careers | darktrace_com.py |
| Proofpoint | https://proofpoint.com/careers | proofpoint_com.py |
| Tenable | https://tenable.com/careers | tenable_com.py |
| Rapid7 | https://rapid7.com/careers | rapid7_com.py |
| Qualys | https://qualys.com/careers | qualys_com.py |
| Acronis | https://acronis.com/careers | acronis_com.py |
| F5 | https://f5.com/careers | f5_com.py |
| Comcast | https://comcast.com/careers | comcast_com.py |
| Reddit | https://redditinc.com/careers | redditinc_com.py |
| Mozilla | https://mozilla.org/careers | mozilla_org.py |
