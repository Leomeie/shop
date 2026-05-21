"""Message Cache Web Dashboard

启动方式：
    python -m cache.dashboard

功能：
    - 实时命中率统计
    - 术语表管理
    - 缓存条目查看
    - API 状态监控
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    import uvicorn
except ImportError:
    print("请先安装: pip install fastapi uvicorn")
    sys.exit(1)

from cache import CacheConfig, MessageCacheService

app = FastAPI(title="Message Cache Dashboard")

_cache_pool: dict[str, MessageCacheService] = {}

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Message Cache Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; }
        .header { background: linear-gradient(135deg, #1e293b, #334155); padding: 24px 32px; border-bottom: 1px solid #475569; }
        .header h1 { font-size: 24px; color: #38bdf8; }
        .header p { color: #94a3b8; margin-top: 4px; font-size: 14px; }
        .container { max-width: 1200px; margin: 0 auto; padding: 24px; }
        .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
        .stat-card { background: #1e293b; border-radius: 12px; padding: 20px; border: 1px solid #334155; }
        .stat-card .label { color: #94a3b8; font-size: 13px; margin-bottom: 8px; }
        .stat-card .value { font-size: 28px; font-weight: 700; }
        .stat-card .value.green { color: #22c55e; }
        .stat-card .value.blue { color: #38bdf8; }
        .stat-card .value.yellow { color: #fbbf24; }
        .stat-card .value.red { color: #f87171; }
        .section { background: #1e293b; border-radius: 12px; padding: 20px; border: 1px solid #334155; margin-bottom: 24px; }
        .section h2 { font-size: 16px; color: #38bdf8; margin-bottom: 16px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #334155; font-size: 14px; }
        th { color: #94a3b8; font-weight: 500; }
        .tag { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
        .tag-exact { background: #166534; color: #22c55e; }
        .tag-fuzzy { background: #1e3a5f; color: #38bdf8; }
        .tag-prefix { background: #713f12; color: #fbbf24; }
        .bar { height: 8px; border-radius: 4px; background: #334155; }
        .bar-fill { height: 100%; border-radius: 4px; transition: width 0.5s; }
        .bar-green { background: #22c55e; }
        .bar-blue { background: #38bdf8; }
        .controls { display: flex; gap: 12px; margin-bottom: 16px; }
        .controls input, .controls select { background: #0f172a; border: 1px solid #475569; color: #e2e8f0; padding: 8px 12px; border-radius: 6px; font-size: 14px; }
        .controls button { background: #38bdf8; color: #0f172a; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600; cursor: pointer; }
        .controls button:hover { background: #7dd3fc; }
        .term-list { display: flex; flex-wrap: wrap; gap: 8px; }
        .term { background: #334155; padding: 4px 10px; border-radius: 6px; font-size: 13px; }
        .term .freq { color: #38bdf8; margin-left: 4px; }
        .empty { color: #64748b; text-align: center; padding: 40px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Message Cache Dashboard</h1>
        <p>实时监控缓存命中率、术语表和系统状态</p>
    </div>
    <div class="container">
        <div class="controls">
            <input type="text" id="apiKey" placeholder="API Key" value="default">
            <input type="text" id="project" placeholder="Project" value="default">
            <button onclick="refresh()">刷新</button>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="label">总查询</div>
                <div class="value blue" id="total">0</div>
            </div>
            <div class="stat-card">
                <div class="label">命中率</div>
                <div class="value green" id="hitRate">0%</div>
            </div>
            <div class="stat-card">
                <div class="label">节省 Tokens</div>
                <div class="value yellow" id="tokens">0</div>
            </div>
            <div class="stat-card">
                <div class="label">节省费用</div>
                <div class="value green" id="cost">$0.00</div>
            </div>
        </div>

        <div class="section">
            <h2>命中分布</h2>
            <div style="display: flex; gap: 20px; margin-bottom: 12px;">
                <div style="flex: 1;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                        <span style="font-size: 13px;">精确匹配</span>
                        <span style="font-size: 13px; color: #22c55e;" id="exactCount">0</span>
                    </div>
                    <div class="bar"><div class="bar-fill bar-green" id="exactBar" style="width: 0%"></div></div>
                </div>
                <div style="flex: 1;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                        <span style="font-size: 13px;">模糊匹配</span>
                        <span style="font-size: 13px; color: #38bdf8;" id="fuzzyCount">0</span>
                    </div>
                    <div class="bar"><div class="bar-fill bar-blue" id="fuzzyBar" style="width: 0%"></div></div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>术语表</h2>
            <div id="glossaryInfo" style="margin-bottom: 12px; font-size: 14px; color: #94a3b8;">
                术语总数: <span id="termCount">0</span> | 高频术语: <span id="highFreqCount">0</span>
            </div>
            <div class="term-list" id="termList">
                <div class="empty">暂无术语</div>
            </div>
        </div>
    </div>

    <script>
        const API = 'http://127.0.0.1:8000';

        async function refresh() {
            const key = document.getElementById('apiKey').value;
            const proj = document.getElementById('project').value;
            try {
                const statsRes = await fetch(`${API}/stats?api_key=${key}&project=${proj}`);
                const stats = await statsRes.json();
                document.getElementById('total').textContent = stats.total_queries || 0;
                const hr = typeof stats.hit_rate === 'string' ? parseFloat(stats.hit_rate) : (stats.hit_rate || 0);
                document.getElementById('hitRate').textContent = (hr * 100).toFixed(1) + '%';
                document.getElementById('tokens').textContent = (stats.tokens_saved || 0).toLocaleString();
                document.getElementById('cost').textContent = '$' + (stats.cost_saved || 0).toFixed(2);

                const total = stats.total_queries || 1;
                const exact = stats.by_source?.exact || 0;
                const fuzzy = stats.by_source?.fuzzy || 0;
                document.getElementById('exactCount').textContent = exact;
                document.getElementById('fuzzyCount').textContent = fuzzy;
                document.getElementById('exactBar').style.width = (exact/total*100) + '%';
                document.getElementById('fuzzyBar').style.width = (fuzzy/total*100) + '%';

                const glossRes = await fetch(`${API}/glossary?api_key=${key}&project=${proj}`);
                const gloss = await glossRes.json();
                document.getElementById('termCount').textContent = gloss.total_terms;
                document.getElementById('highFreqCount').textContent = gloss.high_freq_terms;

                const termList = document.getElementById('termList');
                if (gloss.top_terms && gloss.top_terms.length > 0) {
                    termList.innerHTML = gloss.top_terms.map(t =>
                        `<div class="term">${t.word}<span class="freq">×${t.frequency}</span></div>`
                    ).join('');
                }
            } catch(e) {
                console.error('API 未启动，请先运行: python -m cache.api');
            }
        }

        refresh();
        setInterval(refresh, 5000);
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def dashboard():
    return DASHBOARD_HTML


if __name__ == "__main__":
    print("📊 Message Cache Dashboard 启动中...")
    print("   http://127.0.0.1:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001)
