import { useEffect, useState } from "react";
import {
  ArrowLeft,
  ArrowUpRight,
  Activity,
  Database,
  ExternalLink,
  Play,
  Plus,
  BriefcaseBusiness,
  Check,
  ChevronDown,
  Clock3,
  Filter,
  MapPin,
  RefreshCw,
  Search,
  SlidersHorizontal,
  Sparkles,
} from "lucide-react";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";
const PAGE_SIZE = 24;
type Job = {
  id: number;
  title: string;
  company: string;
  location: string | null;
  location_country: string | null;
  department: string | null;
  employment_type: string | null;
  description: string | null;
  url: string;
  apply_url: string | null;
  posted_at: string | null;
  first_seen_at: string | null;
  last_seen_at: string | null;
  source: string;
  work_mode: string | null;
  required_skills: string[];
  preferred_skills: string[];
  tech_stack: string[];
  salary_min: number | null;
  salary_max: number | null;
  salary_currency: string | null;
  salary_period: string | null;
  compensation_text: string | null;
  education_requirements: string | null;
  experience_min_months: number | null;
  visa_sponsorship: boolean | null;
  relocation_available: boolean | null;
  status: string;
  application_deadline: string | null;
  benefits: string[];
  parser_version: string | null;
};
type Page = {
  items: Job[];
  total: number;
  limit: number;
  offset: number;
  has_more: boolean;
};
type Filters = {
  companies: string[];
  employment_types: string[];
  sources: string[];
  locations: string[];
  work_modes: string[];
  countries: string[];
  skills: string[];
  currencies: string[];
};
type Stats = {
  jobs: number;
  companies: number;
  sources: number;
  runs: number;
  queued: number;
};
const emptyFilters: Filters = {
  companies: [],
  employment_types: [],
  sources: [],
  locations: [],
  work_modes: [],
  countries: [],
  skills: [],
  currencies: [],
};
const emptyStats: Stats = {
  jobs: 0,
  companies: 0,
  sources: 0,
  runs: 0,
  queued: 0,
};

function queryState() {
  const q = new URLSearchParams(location.search);
  return {
    search: q.get("q") || "",
    company: q.get("company") || "",
    type: q.get("type") || "",
    mode: q.get("mode") || "",
    country: q.get("country") || "",
    skill: q.get("skill") || "",
    sort: q.get("sort") || "newest",
    page: Number(q.get("page") || 1) || 1,
  };
}
function formatDate(value: string | null) {
  if (!value) return null;
  const date = new Date(value);
  return Number.isNaN(date.valueOf())
    ? value
    : date.toLocaleDateString(undefined, {
        month: "short",
        day: "numeric",
        year: "numeric",
      });
}
function safeUrl(value: string | null) {
  if (!value) return null;
  try {
    const url = new URL(value);
    return ["http:", "https:"].includes(url.protocol) ? url.toString() : null;
  } catch {
    return null;
  }
}
function humanAge(value: string | null) {
  const date = value && new Date(value);
  if (!date || Number.isNaN(date.valueOf())) return "Recently verified";
  const days = Math.max(
    0,
    Math.floor((Date.now() - date.valueOf()) / 86400000),
  );
  return days === 0 ? "Verified today" : `${days}d ago`;
}

export default function App() {
  const detailId = location.pathname.match(/^\/jobs\/(\d+)$/)?.[1];
  return detailId ? <JobDetail id={detailId} /> : <Directory />;
}

function Directory() {
  const initial = queryState();
  const [jobs, setJobs] = useState<Job[]>([]),
    [total, setTotal] = useState(0),
    [stats, setStats] = useState(emptyStats),
    [filters, setFilters] = useState(emptyFilters);
  const [search, setSearch] = useState(initial.search),
    [company, setCompany] = useState(initial.company),
    [type, setType] = useState(initial.type),
    [mode, setMode] = useState(initial.mode),
    [country, setCountry] = useState(initial.country),
    [skill, setSkill] = useState(initial.skill),
    [sort, setSort] = useState(initial.sort),
    [page, setPage] = useState(initial.page);
  const [loading, setLoading] = useState(true),
    [error, setError] = useState(""),
    [mobileFilters, setMobileFilters] = useState(false),
    [syncing, setSyncing] = useState(false);
  const activeCount = [company, type, mode, country, skill].filter(
    Boolean,
  ).length;
  function reset() {
    setSearch("");
    setCompany("");
    setType("");
    setMode("");
    setCountry("");
    setSkill("");
    setSort("newest");
    setPage(1);
  }
  useEffect(() => {
    const q = new URLSearchParams();
    if (search) q.set("q", search);
    if (company) q.set("company", company);
    if (type) q.set("type", type);
    if (mode) q.set("mode", mode);
    if (country) q.set("country", country);
    if (skill) q.set("skill", skill);
    if (sort !== "newest") q.set("sort", sort);
    if (page > 1) q.set("page", String(page));
    window.history.replaceState(null, "", q.toString() ? `/?${q}` : "/");
  }, [search, company, type, mode, country, skill, sort, page]);
  useEffect(() => {
    const controller = new AbortController();
    const timer = window.setTimeout(async () => {
      setLoading(true);
      setError("");
      try {
        const q = new URLSearchParams({
          limit: String(PAGE_SIZE),
          offset: String((page - 1) * PAGE_SIZE),
          sort,
        });
        if (search) q.set("search", search);
        if (company) q.set("company", company);
        if (type) q.set("employment_type", type);
        if (mode) q.set("work_mode", mode);
        if (country) q.set("country", country);
        if (skill) q.set("skill", skill);
        const responses = await Promise.all([
          fetch(`${API}/api/jobs?${q}`, { signal: controller.signal }),
          fetch(`${API}/api/stats`, { signal: controller.signal }),
          fetch(`${API}/api/filters`, { signal: controller.signal }),
          fetch(`${API}/api/queue`, { signal: controller.signal }),
        ]);
        if (!responses.every((r) => r.ok))
          throw new Error("The local API returned an error.");
        const data: Page = await responses[0].json();
        setJobs(data.items);
        setTotal(data.total);
        setStats({
          ...(await responses[1].json()),
          ...(await responses[3].json()),
        });
        setFilters(await responses[2].json());
      } catch (err) {
        if (err instanceof DOMException && err.name === "AbortError") return;
        setError(
          err instanceof Error ? err.message : "The local API is unavailable.",
        );
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    }, 250);
    return () => {
      window.clearTimeout(timer);
      controller.abort();
    };
  }, [search, company, type, mode, country, skill, sort, page]);
  async function sync() {
    setSyncing(true);
    try {
      const response = await fetch(`${API}/api/connectors/run-all`, {
        method: "POST",
      });
      if (!response.ok) throw new Error("Could not queue a sync.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Sync failed.");
    } finally {
      setSyncing(false);
    }
  }
  return (
    <main className="app-shell">
      <Header onSync={sync} syncing={syncing} />
      <section className="intro">
        <div>
          <p className="kicker">
            <Sparkles size={14} /> LOCAL JOB INDEX
          </p>
          <h1>
            Find work worth
            <br />
            <em>following up on.</em>
          </h1>
          <p className="lede">
            A focused directory of public roles, normalized from the sources you
            trust.
          </p>
        </div>
        <div className="intro-note">
          <strong>{stats.jobs.toLocaleString()}</strong>
          <span>
            active listings
            <br />
            in the local index
          </span>
        </div>
      </section>
      <section className="search-panel">
        <div className="search-wrap">
          <Search size={20} />
          <input
            aria-label="Search jobs"
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            placeholder="Search roles, companies, skills, or technologies"
          />
          <kbd>⌘ K</kbd>
        </div>
        <button
          className="filter-toggle"
          onClick={() => setMobileFilters(!mobileFilters)}
        >
          <Filter size={16} /> Filters{" "}
          {activeCount ? <b>{activeCount}</b> : null}
        </button>
      </section>
      <div
        className={`directory-layout ${mobileFilters ? "filters-open" : ""}`}
      >
        <aside className="filters">
          <div className="filters-title">
            <span>
              <SlidersHorizontal size={16} /> Refine results
            </span>
            <button onClick={reset}>Reset</button>
          </div>
          <FilterSelect
            label="Company"
            value={company}
            options={filters.companies}
            onChange={(v) => {
              setCompany(v);
              setPage(1);
            }}
          />
          <FilterSelect
            label="Employment"
            value={type}
            options={filters.employment_types}
            onChange={(v) => {
              setType(v);
              setPage(1);
            }}
          />
          <FilterSelect
            label="Work mode"
            value={mode}
            options={filters.work_modes}
            onChange={(v) => {
              setMode(v);
              setPage(1);
            }}
          />
          <FilterSelect
            label="Country"
            value={country}
            options={filters.countries}
            onChange={(v) => {
              setCountry(v);
              setPage(1);
            }}
          />
          <FilterSelect
            label="Skill or technology"
            value={skill}
            options={filters.skills}
            onChange={(v) => {
              setSkill(v);
              setPage(1);
            }}
          />
          <button
            className="close-filters"
            onClick={() => setMobileFilters(false)}
          >
            Show {total.toLocaleString()} results <Check size={15} />
          </button>
        </aside>
        <section className="results">
          <div className="results-head">
            <div>
              <p className="kicker">DISCOVERY FEED</p>
              <h2>
                {total.toLocaleString()} <span>matching roles</span>
              </h2>
            </div>
            <label className="sort">
              Sort by{" "}
              <select
                value={sort}
                onChange={(e) => {
                  setSort(e.target.value);
                  setPage(1);
                }}
              >
                <option value="newest">Recently verified</option>
                <option value="relevance">Relevance</option>
                <option value="deadline">Application deadline</option>
              </select>
              <ChevronDown size={14} />
            </label>
          </div>
          {error ? (
            <div className="state error-state">
              <h3>Could not load listings</h3>
              <p>{error}</p>
              <button
                className="button primary-button"
                onClick={() => setPage(page)}
              >
                Retry
              </button>
            </div>
          ) : loading ? (
            <Skeletons />
          ) : jobs.length ? (
            <>
              <div className="job-list">
                {jobs.map((job) => (
                  <JobCard key={job.id} job={job} />
                ))}
              </div>
              <Pagination page={page} total={total} onChange={setPage} />
            </>
          ) : (
            <div className="state">
              <BriefcaseBusiness size={26} />
              <h3>No roles match those filters</h3>
              <p>
                Try widening your search or clear one of the active filters.
              </p>
              <button className="button outline-button" onClick={reset}>
                Clear filters
              </button>
            </div>
          )}
        </section>
      </div>
      <footer>
        <span>OPENAPPLYBOT / LOCAL JOB INDEX</span>
        <span>
          {stats.companies} companies · {stats.sources} sources · {stats.queued}{" "}
          queued
        </span>
        <a href={`${API}/docs`} target="_blank" rel="noreferrer">
          API docs <ArrowUpRight size={13} />
        </a>
      </footer>
    </main>
  );
}

function Header({ onSync, syncing }: { onSync: () => void; syncing: boolean }) {
  return (
    <header className="header">
      <a href="/" className="brand">
        <span className="brand-mark">
          <BriefcaseBusiness size={18} />
        </span>
        <span>
          OpenApply<em>Bot</em>
          <small>JOBS INTELLIGENCE</small>
        </span>
      </a>
      <nav>
        <a href="/">Explore</a>
        <a href="/sources">Sources</a>
        <a href="/runs">Run history</a>
        <button
          className="button primary-button"
          onClick={onSync}
          disabled={syncing}
        >
          <RefreshCw size={15} className={syncing ? "spin" : ""} />{" "}
          {syncing ? "Queuing" : "Refresh sources"}
        </button>
      </nav>
    </header>
  );
}
function FilterSelect({
  label,
  value,
  options,
  onChange,
}: {
  label: string;
  value: string;
  options: string[];
  onChange: (value: string) => void;
}) {
  return (
    <label className="filter-field">
      <span>{label}</span>
      <select value={value} onChange={(e) => onChange(e.target.value)}>
        <option value="">All {label.toLowerCase()}s</option>
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
      <ChevronDown size={14} />
    </label>
  );
}
function JobCard({ job }: { job: Job }) {
  const skills = [
    ...new Set([...(job.required_skills || []), ...(job.tech_stack || [])]),
  ].slice(0, 4);
  return (
    <article className="job-card">
      <div className="company-avatar">
        {job.company.slice(0, 1).toUpperCase()}
      </div>
      <div className="job-card-body">
        <div className="job-card-top">
          <div>
            <a className="job-title" href={`/jobs/${job.id}`}>
              {job.title}
            </a>
            <p className="company-name">{job.company}</p>
          </div>
          <span className={`status status-${job.status}`}>
            {job.status === "open" ? "Open" : "Unverified"}
          </span>
        </div>
        <div className="job-facts">
          {job.location ? (
            <span>
              <MapPin size={14} /> {job.location}
            </span>
          ) : (
            <span>
              <MapPin size={14} /> Location not listed
            </span>
          )}
          {job.work_mode && <span>{job.work_mode}</span>}
          {job.employment_type && <span>{job.employment_type}</span>}
          <span>
            <Clock3 size={14} />{" "}
            {humanAge(job.last_seen_at || job.first_seen_at)}
          </span>
        </div>
        {skills.length > 0 && (
          <div className="skill-row">
            {skills.map((skill) => (
              <span key={skill}>{skill}</span>
            ))}
          </div>
        )}
      </div>
      <a
        className="card-arrow"
        href={`/jobs/${job.id}`}
        aria-label={`View ${job.title}`}
      >
        <ArrowUpRight size={18} />
      </a>
    </article>
  );
}
function Skeletons() {
  return (
    <div className="job-list">
      {Array.from({ length: 5 }, (_, index) => (
        <div className="job-card skeleton" key={index}>
          <i />
          <div>
            <b />
            <span />
            <small />
          </div>
        </div>
      ))}
    </div>
  );
}
function Pagination({
  page,
  total,
  onChange,
}: {
  page: number;
  total: number;
  onChange: (page: number) => void;
}) {
  const pages = Math.max(1, Math.ceil(total / PAGE_SIZE));
  return (
    <div className="pagination">
      <button
        className="button outline-button"
        disabled={page <= 1}
        onClick={() => onChange(page - 1)}
      >
        Previous
      </button>
      <span>
        Page {page} of {pages}
      </span>
      <button
        className="button outline-button"
        disabled={page >= pages}
        onClick={() => onChange(page + 1)}
      >
        Next
      </button>
    </div>
  );
}
function JobDetail({ id }: { id: string }) {
  const [job, setJob] = useState<Job | null>(null),
    [loading, setLoading] = useState(true),
    [error, setError] = useState("");
  useEffect(() => {
    const controller = new AbortController();
    fetch(`${API}/api/jobs/${id}`, { signal: controller.signal })
      .then((response) => {
        if (response.status === 404)
          throw new Error("This listing no longer exists in the local index.");
        if (!response.ok) throw new Error("Could not load this listing.");
        return response.json();
      })
      .then(setJob)
      .catch((err) => {
        if (err.name !== "AbortError") setError(err.message);
      })
      .finally(() => setLoading(false));
    return () => controller.abort();
  }, [id]);
  if (loading)
    return (
      <main className="app-shell">
        <Header onSync={() => undefined} syncing={false} />
        <div className="detail-loading">
          <RefreshCw className="spin" /> Loading listing
        </div>
      </main>
    );
  if (error || !job)
    return (
      <main className="app-shell">
        <Header onSync={() => undefined} syncing={false} />
        <div className="state error-state">
          <h2>Listing unavailable</h2>
          <p>{error}</p>
          <a className="button outline-button" href="/">
            <ArrowLeft size={15} /> Back to directory
          </a>
        </div>
      </main>
    );
  const apply = safeUrl(job.apply_url || job.url);
  return (
    <main className="app-shell">
      <Header onSync={() => undefined} syncing={false} />
      <article className="detail">
        <a className="back-link" href="/">
          <ArrowLeft size={15} /> Back to directory
        </a>
        <header className="detail-header">
          <div className="company-avatar large">
            {job.company.slice(0, 1).toUpperCase()}
          </div>
          <div>
            <p className="kicker">
              {job.source} · {humanAge(job.last_seen_at || job.first_seen_at)}
            </p>
            <h1>{job.title}</h1>
            <p className="detail-company">
              {job.company} {job.location && ` · ${job.location}`}
            </p>
          </div>
          {apply && (
            <a
              className="button primary-button apply-button"
              href={apply}
              target="_blank"
              rel="noreferrer"
            >
              Apply on source <ArrowUpRight size={16} />
            </a>
          )}
        </header>
        <div className="detail-grid">
          <div className="detail-main">
            <section>
              <h2>About the role</h2>
              <div className="description">
                {job.description ||
                  "The source did not provide a full description."}
              </div>
            </section>
            {job.required_skills?.length || job.tech_stack?.length ? (
              <section>
                <h2>Skills and technologies</h2>
                <div className="detail-tags">
                  {[
                    ...new Set([
                      ...(job.required_skills || []),
                      ...(job.tech_stack || []),
                    ]),
                  ].map((skill) => (
                    <span key={skill}>{skill}</span>
                  ))}
                </div>
              </section>
            ) : null}
          </div>
          <aside className="detail-aside">
            <Info
              label="Work arrangement"
              value={job.work_mode || "Not specified"}
            />
            <Info
              label="Employment"
              value={job.employment_type || "Not specified"}
            />
            <Info
              label="Posted"
              value={formatDate(job.posted_at) || "Date not provided"}
            />
            <Info
              label="Verified"
              value={
                formatDate(job.last_seen_at || job.first_seen_at) ||
                "Not available"
              }
            />
            <Info
              label="Experience"
              value={
                job.experience_min_months
                  ? `${job.experience_min_months / 12}+ years`
                  : "Not specified"
              }
            />
            <Info
              label="Education"
              value={job.education_requirements || "Not specified"}
            />
            {job.compensation_text && (
              <Info label="Compensation" value={job.compensation_text} />
            )}
          </aside>
        </div>
        <p className="source-note">
          This listing is collected from a public source. Application links open
          the original website; OpenApplyBot does not submit applications.
        </p>
      </article>
    </main>
  );
}
function Info({ label, value }: { label: string; value: string }) {
  return (
    <div className="info">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}


type SourceRow = {
  id: number; company: string; careers_url: string | null; connector: string;
  board_token: string; active: boolean; last_run_at: string | null; last_error: string | null;
};
type RunRow = {
  id: number; source_id: number | null; connector: string; started_at: string;
  finished_at: string | null; fetched: number; inserted: number; updated: number;
  status: string; error: string | null;
};

function SourcesPage() {
  const [sources, setSources] = useState<SourceRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [busy, setBusy] = useState<number | null>(null);
  const [company, setCompany] = useState("");
  const [url, setUrl] = useState("");
  const [connector, setConnector] = useState("auto");
  const [token, setToken] = useState("");
  const [adding, setAdding] = useState(false);
  async function load() {
    setLoading(true);
    try {
      const r = await fetch(`${API}/api/sources`);
      if (!r.ok) throw new Error("Could not load sources from the local API.");
      setSources(await r.json()); setError("");
    } catch (e) { setError(e instanceof Error ? e.message : "Request failed."); }
    finally { setLoading(false); }
  }
  useEffect(() => { void load(); }, []);
  async function addSource(e: React.FormEvent) {
    e.preventDefault(); setAdding(true); setError(""); setNotice("");
    try {
      const r = await fetch(`${API}/api/sources`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({company_name:company,careers_url:url,connector,board_token:token || undefined})});
      const body = await r.json();
      if (!r.ok) throw new Error(body.detail || "Could not add source.");
      setCompany(""); setUrl(""); setToken(""); setNotice("Source registered. You can queue it when ready."); await load();
    } catch (e) { setError(e instanceof Error ? e.message : "Request failed."); }
    finally { setAdding(false); }
  }
  async function runSource(id:number) {
    setBusy(id); setError(""); setNotice("");
    try {
      const r = await fetch(`${API}/api/sources/${id}/run`, {method:"POST"});
      const body = await r.json();
      if (!r.ok) throw new Error(body.detail || "Could not queue source.");
      setNotice(`Source #${id} queued successfully.`);
    } catch (e) { setError(e instanceof Error ? e.message : "Request failed."); }
    finally { setBusy(null); }
  }
  return <main className="app-shell">
    <Header onSync={async()=>{try{const r=await fetch(`${API}/api/connectors/run-all`,{method:"POST"});if(!r.ok)throw new Error("Could not queue scrapers.");setNotice("All active sources queued.");}catch(e){setError(e instanceof Error?e.message:"Request failed.");}}} syncing={false}/>
    <section className="page-heading"><p className="kicker"><Database size={14}/> INGESTION CONTROL</p><h1>Source <em>registry.</em></h1><p className="lede">Manage public job feeds and employer career pages connected to your local index.</p></section>
    {error && <div className="notice error-state">{error}</div>}{notice && <div className="notice success-state">{notice}</div>}
    <section className="panel">
      <h2><Plus size={18}/> Register a source</h2>
      <form className="source-form" onSubmit={addSource}>
        <label>Company name<input required value={company} onChange={e=>setCompany(e.target.value)} placeholder="Example: Example Inc."/></label>
        <label>Public careers URL<input type="url" value={url} onChange={e=>setUrl(e.target.value)} placeholder="https://company.com/careers"/></label>
        <label>Connector<select value={connector} onChange={e=>setConnector(e.target.value)}>{["auto","jsonld","greenhouse","lever","ashby","smartrecruiters","workable","recruitee","workday","remoteok","remotive","arbeitnow","themuse","jobicy","himalayas"].map(x=><option key={x}>{x}</option>)}</select></label>
        <label>Board ID / keyword<input value={token} onChange={e=>setToken(e.target.value)} placeholder={["auto","jsonld","workday"].includes(connector)?"Optional; defaults to careers URL":"Required for this connector"}/></label>
        <button className="button primary-button" disabled={adding}><Plus size={15}/>{adding?"Adding source…":"Add source"}</button>
      </form>
      <p className="muted-note">Use verified public board IDs for ATS connectors. Auto-discovery does not guarantee every website is crawlable.</p>
    </section>
    <section className="panel">
      <div className="panel-heading"><h2>Registered sources <span>{sources.length}</span></h2><button className="button outline-button" onClick={()=>void load()}>Refresh list</button></div>
      {loading ? <p className="muted-note">Loading sources…</p> : sources.length===0 ? <p className="muted-note">No sources yet. Add one above or run the scraper command to seed the employer registry.</p> :
        <div className="table-scroll"><table className="data-table"><thead><tr><th>Company / source</th><th>Connector</th><th>Last run</th><th>State</th><th></th></tr></thead><tbody>{sources.map(s=><tr key={s.id}><td><strong>{s.company}</strong><small>{s.careers_url || s.board_token}</small>{s.last_error && <small className="error-text">{s.last_error}</small>}</td><td><code>{s.connector}</code></td><td>{s.last_run_at ? formatDate(s.last_run_at) : "Never"}</td><td><span className={`status ${s.last_error?"status-unverified":"status-open"}`}>{s.last_error?"Error":s.active?"Active":"Inactive"}</span></td><td><button className="button outline-button" disabled={!s.active || busy===s.id} onClick={()=>void runSource(s.id)}><Play size={13}/>{busy===s.id?"Queueing":"Run"}</button></td></tr>)}</tbody></table></div>}
    </section>
    <footer><span>LOCAL-FIRST · SOURCE CONTROL</span><a href="/runs">View run history <ExternalLink size={13}/></a><a href="/">Back to jobs</a></footer>
  </main>;
}

function RunsPage() {
  const [runs,setRuns] = useState<RunRow[]>([]);
  const [loading,setLoading] = useState(true);
  const [error,setError] = useState("");
  async function load() {
    setLoading(true);
    try { const r=await fetch(`${API}/api/runs?limit=100`); if(!r.ok)throw new Error("Could not load run history."); setRuns(await r.json()); setError(""); }
    catch(e){setError(e instanceof Error?e.message:"Request failed.");}
    finally{setLoading(false);}
  }
  useEffect(()=>{void load();const timer=window.setInterval(()=>void load(),15000);return()=>window.clearInterval(timer);},[]);
  return <main className="app-shell">
    <Header onSync={async()=>{await fetch(`${API}/api/connectors/run-all`,{method:"POST"});}} syncing={false}/>
    <section className="page-heading"><p className="kicker"><Activity size={14}/> PIPELINE OBSERVABILITY</p><h1>Run <em>history.</em></h1><p className="lede">Recent scraper executions, fetched records, changes and failures. Refreshes every 15 seconds.</p></section>
    {error && <div className="notice error-state">{error}</div>}
    <section className="panel"><div className="panel-heading"><h2>Recent executions <span>{runs.length}</span></h2><button className="button outline-button" onClick={()=>void load()}>Refresh</button></div>
    {loading ? <p className="muted-note">Loading run history…</p> : runs.length===0 ? <p className="muted-note">No scraper runs recorded yet. Queue sources from the source registry.</p> :
      <div className="table-scroll"><table className="data-table"><thead><tr><th>Started</th><th>Connector</th><th>Source</th><th>Fetched</th><th>Inserted</th><th>Updated</th><th>Status</th></tr></thead><tbody>{runs.map(r=><tr key={r.id}><td>{formatDate(r.started_at)}</td><td><code>{r.connector}</code></td><td>{r.source_id ?? "—"}</td><td>{r.fetched}</td><td>{r.inserted}</td><td>{r.updated}</td><td><span className={`status ${r.status==="success"?"status-open":"status-unverified"}`}>{r.status}</span>{r.error&&<small className="error-text">{r.error}</small>}</td></tr>)}</tbody></table></div>}
    </section>
    <footer><span>LOCAL-FIRST · PIPELINE HEALTH</span><a href="/sources">Manage sources</a><a href="/">Back to jobs</a></footer>
  </main>;
}
