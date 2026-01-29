from datetime import datetime
import html

# ===================== CONFIG =====================

GROUP_SKINS = {
    "RNC Cluster": {"bg": "#e3f2fd", "border": "#1565c0"},
    "DGX Servers": {"bg": "#ede7f6", "border": "#5e35b1"},
    "License Servers": {"bg": "#e8f5e9", "border": "#2e7d32"},
    "NIS Servers": {"bg": "#fff3e0", "border": "#ef6c00"},
    "DEFAULT": {"bg": "#f5f7fa", "border": "#90a4ae"},
}

ROLE_BADGE = {
    "login": ("LOGIN", "#0288d1"),
    "compute": ("COMPUTE", "#6a1b9a"),
    "gpu": ("GPU", "#f9a825"),
    "storage": ("STORAGE", "#2e7d32"),
    "default": ("NODE", "#546e7a"),
}

SEVERITY_STYLE = {
    "OK": ("🟢 OK", "#1e8e3e"),
    "CRITICAL": ("🔴 CRITICAL", "#d93025"),
}

# ===================== HELPERS =====================

def severity(row):
    return "CRITICAL" if row["is_issue"] else "OK"

def node_state(row):
    return "🔴 DOWN" if row["is_issue"] else "🟢 UP"

# ===================== MAIN =====================

def build_report_html(results: dict, overall_issues: int):

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    healthy = overall_issues == 0
    total_nodes = sum(len(d["rows"]) for d in results.values())

    html_report = f"""
    <style>
        body {{
            font-family: Segoe UI, Arial, sans-serif;
            background: #ffffff;
            color: #222;
        }}

        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0 10px;
            font-size: 14px;
        }}

        th {{
            background: #eceff1;
            padding: 10px;
            text-align: left;
        }}

        td {{
            padding: 10px;
            background: #ffffff;
        }}

        .table-wrapper {{
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }}

        @media only screen and (max-width: 768px) {{
            table {{
                min-width: 900px;
            }}
        }}
    </style>

    <div style="max-width:1150px;margin:auto;">

    <div style="padding:22px;border-radius:14px;
                background:{'#e6f4ea' if healthy else '#fdecea'};
                border:2px solid {'#1e8e3e' if healthy else '#d93025'};">
        <h1 style="margin:0;">Infrastructure Monitoring Report</h1>
        <p>Generated: <b>{ts}</b></p>
        <span style="padding:6px 18px;border-radius:20px;
                     background:{'#34a853' if healthy else '#d93025'};
                     color:white;font-weight:600;">
            {"ALL SYSTEMS HEALTHY" if healthy else f"{overall_issues} ACTIVE ISSUE(S)"}
        </span>
    </div>

    <div style="margin-top:18px;padding:16px;background:#f7f9fc;
                border-radius:12px;border:1px solid #d0d7de;">
        <b>Total Nodes:</b> {total_nodes} &nbsp;&nbsp;
        <b>Issues:</b> {overall_issues}
    </div>
    """

    for group, data in results.items():
        skin = GROUP_SKINS.get(group, GROUP_SKINS["DEFAULT"])

        html_report += f"""
        <div style="margin-top:26px;">
            <div style="padding:14px;border-radius:12px;
                        background:{skin['bg']};
                        border-left:6px solid {skin['border']};
                        font-size:18px;font-weight:700;">
                {group} — {data["issues"]} issue(s)
            </div>

            <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th>Node</th>
                        <th>Role</th>
                        <th>IP</th>
                        <th>Status</th>
                        <th>Ping</th>
                        <th>SSH</th>
                        <th>Last Seen</th>
                        <th>Node State</th>
                    </tr>
                </thead>
                <tbody>
        """

        for r in data["rows"]:
            sev = severity(r)
            sev_text, sev_color = SEVERITY_STYLE[sev]
            role = r.get("role", "default")
            role_text, role_color = ROLE_BADGE.get(role, ROLE_BADGE["default"])

            html_report += f"""
                <tr style="border-left:6px solid {sev_color};">
                    <td><b>{html.escape(r["name"])}</b></td>
                    <td>
                        <span style="padding:4px 10px;border-radius:12px;
                                     background:{role_color};
                                     color:white;font-size:12px;font-weight:600;">
                            {role_text}
                        </span>
                    </td>
                    <td>{r["ip"]}</td>
                    <td style="color:{sev_color};font-weight:700;">{sev_text}</td>
                    <td>{r["ping"]}</td>
                    <td>{r["ssh"]}</td>
                    <td>{r["last_seen"]}</td>
                    <td><b>{node_state(r)}</b></td>
                </tr>
            """

        html_report += """
                </tbody>
            </table>
            </div>
        </div>
        """

    html_report += """
        <div style="margin-top:30px;padding:14px;font-size:12px;color:#555;">
            Automated report generated by <b>SERC Resource Monitor</b>.
        </div>
    </div>
    """

    return html_report

