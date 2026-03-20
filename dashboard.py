import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

from database import Database, Post, Analytics
from tiktok_client import TikTokContentPlanner
from link_tracker import LinkTracker

# Page Config
st.set_page_config(
    page_title="Elternratgeber Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .revenue-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


class Dashboard:
    def __init__(self):
        self.db = Database()
        self.planner = TikTokContentPlanner()
        self.link_tracker = LinkTracker()
    
    def run(self):
        st.markdown('<div class="main-header">📊 Elternratgeber Marketing Dashboard</div>', unsafe_allow_html=True)
        st.caption("TikTok Automation & Conversion Tracking")
        
        # Sidebar
        with st.sidebar:
            st.header("⚙️ Navigation")
            page = st.radio("", [
                "📈 Übersicht",
                "📝 Content Planer",
                "📊 Analytics",
                "💰 Conversions",
                "⚙️ Einstellungen"
            ])
            
            st.divider()
            st.header("🔑 API Status")
            
            # TikTok API Config
            st.header("🔗 TikTok API")
            
            if 'tiktok_access_token' not in st.session_state:
                st.session_state.tiktok_access_token = ""
            
            tiktok_key = st.text_input(
                "TikTok Access Token",
                value=st.session_state.tiktok_access_token,
                type="password"
            )
            st.session_state.tiktok_access_token = tiktok_key
            
            if tiktok_key:
                st.success("✅ TikTok API Key gesetzt")
            else:
                st.warning("⚠️ Token fehlt - siehe TIKTOK_SETUP.md")
        
        # Main Content
        if page == "📈 Übersicht":
            self.overview_page()
        elif page == "📝 Content Planer":
            self.content_planner_page()
        elif page == "📊 Analytics":
            self.analytics_page()
        elif page == "💰 Conversions":
            self.conversions_page()
        elif page == "⚙️ Einstellungen":
            self.settings_page()
    
    def overview_page(self):
        """Haupt-Dashboard mit KPIs"""
        
        # Stats laden
        stats = self.db.get_dashboard_stats()
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>👁️ Views (30d)</h3>
                    <h2>{stats['engagement_30d']['views']:,}</h2>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>❤️ Likes (30d)</h3>
                    <h2>{stats['engagement_30d']['likes']:,}</h2>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>🔗 Link Clicks</h3>
                    <h2>{stats['engagement_30d']['link_clicks']:,}</h2>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="revenue-card">
                    <h3>💰 Revenue (30d)</h3>
                    <h2>€{stats['revenue_30d']:.2f}</h2>
                </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Content-Übersicht
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📝 Content Status")
            
            post_data = {
                'Status': ['Published', 'Draft', 'Scheduled'],
                'Anzahl': [
                    stats['posts']['published'],
                    stats['posts']['draft'],
                    0  # TODO: scheduled count
                ]
            }
            fig = px.pie(
                post_data, 
                values='Anzahl', 
                names='Status',
                color_discrete_sequence=['#00C851', '#ffbb33', '#33b5e5']
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 Conversion Funnel")
            
            views = stats['engagement_30d']['views']
            clicks = stats['engagement_30d']['link_clicks']
            # Geschätzte Conversions (du musst das manuell tracken)
            
            funnel_data = {
                'Stage': ['Views', 'Profile Visits', 'Link Clicks', 'Sales'],
                'Count': [
                    views,
                    stats['engagement_30d']['profile_visits'],
                    clicks,
                    int(stats['revenue_30d'] / 19)  # Bei 19€ Preis
                ]
            }
            
            fig = px.funnel(
                funnel_data,
                x='Count',
                y='Stage',
                color_discrete_sequence=['#667eea']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Post Performance Table
        st.divider()
        st.subheader("📋 Letzte Posts")
        
        posts = self.db.get_all_posts()
        if posts:
            post_df = pd.DataFrame([
                {
                    'ID': p.id,
                    'Pillar': p.content_pillar,
                    'Hook': p.hook[:50] + '...' if len(p.hook) > 50 else p.hook,
                    'Status': p.status,
                    'Created': p.created_at[:10]
                }
                for p in posts[:10]
            ])
            st.dataframe(post_df, use_container_width=True)
        else:
            st.info("Noch keine Posts vorhanden. Gehe zum Content Planer!")
    
    def content_planner_page(self):
        """Content Erstellung und Planung"""
        
        st.subheader("🎯 Content Generator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Automatische Generierung")
            
            pillar = st.selectbox(
                "Content Pillar",
                options=list(self.planner.CONTENT_PILLARS.keys()),
                format_func=lambda x: self.planner.CONTENT_PILLARS[x]['title']
            )
            
            if st.button("🎲 Carousel-Idee generieren", type="primary"):
                with st.spinner("Generiere..."):
                    data = self.planner.generate_carousel_post(pillar)
                    
                    # Speichern in Session
                    st.session_state.generated_content = data
                    
                    # Auto-generiere Link
                    link = self.link_tracker.create_link(
                        original_url="https://elternratgeber-deploy.vercel.app/",
                        utm_content=f"{pillar}_{datetime.now().strftime('%Y%m%d')}"
                    )
                    st.session_state.generated_link = link
                    
                    st.success("✅ Content + Tracking Link generiert!")
            
            if 'generated_content' in st.session_state:
                data = st.session_state.generated_content
                
                st.markdown("---")
                st.markdown("### 📝 Generierter Content")
                
                st.markdown(f"**Hook:** {data['title']}")
                st.markdown(f"**Pillar:** {data['pillar_title']}")
                
                # Link anzeigen
                if 'generated_link' in st.session_state:
                    link = st.session_state.generated_link
                    short_url = self.link_tracker.get_short_url(
                        link.short_code, 
                        "https://dein-domain.com/r"  # Passe das an!
                    )
                    st.markdown(f"**🔗 Shortlink:** `{short_url}`")
                    st.code(short_url, language=None)
                
                with st.expander("Slide-Struktur"):
                    for i, slide in enumerate(data['slide_structure'], 1):
                        st.markdown(f"{i}. {slide}")
                
                # Speichern Button
                if st.button("💾 In Datenbank speichern"):
                    post = Post(
                        content_pillar=data['pillar'],
                        hook=data['title'],
                        caption=data['title'],  # Caption = Title bei TikTok
                        hashtags=json.dumps(data['suggested_hashtags']),
                        status='draft',
                        image_paths=json.dumps([f"slide_{i}.jpg" for i in range(1, data['slide_count']+1)])
                    )
                    post_id = self.db.create_post(post)
                    
                    # Link mit Post verknüpfen
                    if 'generated_link' in st.session_state:
                        link = st.session_state.generated_link
                        link.post_id = post_id
                    
                    st.success(f"✅ Post #{post_id} gespeichert!")
        
        with col2:
            st.markdown("### 📤 Upload zu TikTok")
            
            if not st.session_state.get('tiktok_access_token'):
                st.warning("⚠️ Bitte TikTok Token in der Sidebar eingeben")
                st.markdown("[Setup Guide](TIKTOK_SETUP.md)")
            else:
                st.success("TikTok API bereit ✅")
                
                # Draft Posts laden
                draft_posts = self.db.get_all_posts(status='draft')
                
                if draft_posts:
                    selected_post = st.selectbox(
                        "Draft auswählen",
                        options=draft_posts,
                        format_func=lambda p: f"#{p.id}: {p.hook[:40]}..."
                    )
                    
                    # Shortlink für diesen Post
                    post_links = self.link_tracker.get_all_links(selected_post.id if selected_post else None)
                    if post_links:
                        st.info(f"🔗 {len(post_links)} Link(s) für diesen Post")
                        for link in post_links[:1]:
                            st.code(self.link_tracker.get_short_url(link.short_code), language=None)
                    
                    schedule_date = st.date_input("Schedule Datum", datetime.now())
                    schedule_time = st.time_input("Schedule Zeit", datetime.strptime("19:00", "%H:%M").time())
                    
                    if st.button("🚀 Als Draft zu TikTok hochladen", type="primary"):
                        with st.spinner("Upload läuft..."):
                            st.info("⚠️ Upload-Funktion implementieren:")
                            st.code(f"""
from tiktok_client import TikTokAPIClient

client = TikTokAPIClient(access_token="{st.session_state.tiktok_access_token}")

result = client.upload_carousel_draft(
    image_paths={json.loads(selected_post.image_paths) if selected_post and selected_post.image_paths else []},
    title="{selected_post.caption[:50] if selected_post else ''}...",
    privacy_level="SELF_ONLY",  # Als Draft
    auto_add_music=True
)

# Status prüfen
status = client.check_upload_status(result['publish_id'])
print(f"Status: {{status['status']}}")
                            """, language="python")
                            
                            st.success("✅ Code-Vorlage generiert!")
                else:
                    st.info("Keine Drafts vorhanden. Generiere erst Content!")
        
        # Content Kalender
        st.divider()
        st.subheader("📆 Content Kalender (Wöchentlich)")
        
        schedule = self.planner.get_weekly_schedule()
        
        cols = st.columns(4)
        for i, post in enumerate(schedule):
            with cols[i % 4]:
                st.markdown(f"**{post['day']}**")
                st.markdown(f"_{post['pillar_title']}_")
                st.markdown(f"📝 {post['title'][:60]}...")
                st.markdown(f"⏰ {post['optimal_posting_time']} Uhr")
                st.divider()
    
    def analytics_page(self):
        """Detaillierte Analytics"""
        
        st.subheader("📊 Post Performance")
        
        posts = self.db.get_all_posts(status='published')
        
        if not posts:
            st.info("Noch keine veröffentlichten Posts.")
            return
        
        # Post Auswahl
        selected = st.selectbox(
            "Post auswählen",
            posts,
            format_func=lambda p: f"#{p.id}: {p.hook[:50]}..."
        )
        
        if selected:
            analytics = self.db.get_analytics_history(selected.id, days=30)
            
            if analytics:
                # Metrics über Zeit
                df = pd.DataFrame([
                    {
                        'Datum': a.recorded_at[:10],
                        'Views': a.views,
                        'Likes': a.likes,
                        'Comments': a.comments,
                        'Shares': a.shares
                    }
                    for a in analytics
                ])
                
                # Line Chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df['Datum'], y=df['Views'], name='Views', mode='lines'))
                fig.add_trace(go.Scatter(x=df['Datum'], y=df['Likes'], name='Likes', mode='lines'))
                fig.add_trace(go.Scatter(x=df['Datum'], y=df['Comments'], name='Comments', mode='lines'))
                
                fig.update_layout(title='Engagement über Zeit', xaxis_title='Datum', yaxis_title='Count')
                st.plotly_chart(fig, use_container_width=True)
                
                # Aktuelle Stats
                latest = analytics[-1]
                cols = st.columns(5)
                cols[0].metric("Views", latest.views)
                cols[1].metric("Likes", latest.likes)
                cols[2].metric("Comments", latest.comments)
                cols[3].metric("Shares", latest.shares)
                cols[4].metric("Link Clicks", latest.link_clicks)
                
                # Engagement Rate
                if latest.views > 0:
                    engagement_rate = ((latest.likes + latest.comments + latest.shares) / latest.views) * 100
                    st.metric("Engagement Rate", f"{engagement_rate:.2f}%")
            else:
                st.info("Noch keine Analytics-Daten für diesen Post.")
    
    def conversions_page(self):
        """Sales & Conversion Tracking"""
        
        st.subheader("💰 Conversion Tracking")
        
        # Manuelle Conversion Eingabe
        with st.expander("➕ Conversion manuell hinzufügen"):
            col1, col2 = st.columns(2)
            
            with col1:
                source = st.text_input("Quelle", value="tiktok")
                utm_campaign = st.text_input("UTM Campaign", value="elternratgeber_launch")
                
                # Post-Auswahl für UTM Content
                posts = self.db.get_all_posts()
                if posts:
                    selected_post = st.selectbox(
                        "Zugeordneter Post (optional)",
                        options=[None] + posts,
                        format_func=lambda p: "Keiner" if p is None else f"#{p.id}: {p.hook[:30]}..."
                    )
                    utm_content = f"post_{selected_post.id}" if selected_post else ""
                else:
                    utm_content = st.text_input("UTM Content (Post ID)", placeholder="z.B. post_123")
            
            with col2:
                revenue = st.number_input("Revenue (€)", value=19.0, step=19.0)
                product = st.selectbox("Produkt", ["elternratgeber", "coaching", "other"])
            
            if st.button("💾 Conversion speichern"):
                from database import Conversion
                conv = Conversion(
                    source=source,
                    utm_campaign=utm_campaign,
                    utm_content=utm_content if isinstance(utm_content, str) else f"post_{selected_post.id}",
                    revenue=revenue,
                    product=product
                )
                self.db.record_conversion(conv)
                st.success("✅ Conversion gespeichert!")
                st.rerun()
        
        # Conversion Übersicht
        conversions = self.db.get_conversions(days=30)
        
        if conversions:
            st.markdown("### 📋 Letzte Conversions")
            
            conv_df = pd.DataFrame([
                {
                    'Datum': c.timestamp[:10],
                    'Quelle': c.source,
                    'UTM': c.utm_content,
                    'Produkt': c.product,
                    'Revenue': f"€{c.revenue:.2f}"
                }
                for c in conversions[:20]
            ])
            st.dataframe(conv_df, use_container_width=True)
            
            # Revenue by Source
            st.markdown("### 📊 Revenue by Source")
            source_data = {}
            for c in conversions:
                source_data[c.source] = source_data.get(c.source, 0) + c.revenue
            
            fig = px.pie(
                names=list(source_data.keys()),
                values=list(source_data.values()),
                title="Revenue Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Noch keine Conversions erfasst.")
        
        # ROI Berechnung
        st.divider()
        st.markdown("### 🧮 ROI Berechnung")
        
        total_revenue = self.db.get_total_revenue(30)
        estimated_ad_spend = st.number_input("Geschätzte Ad Spend (€)", value=0.0)
        time_invested = st.number_input("Zeit investiert (Stunden)", value=10.0)
        hourly_rate = st.number_input("Stundensatz (€)", value=50.0)
        
        total_cost = estimated_ad_spend + (time_invested * hourly_rate)
        roi = ((total_revenue - total_cost) / total_cost * 100) if total_cost > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Revenue", f"€{total_revenue:.2f}")
        col2.metric("Total Cost", f"€{total_cost:.2f}")
        col3.metric("ROI", f"{roi:.1f}%", delta=f"€{total_revenue - total_cost:.2f}")
    
    def settings_page(self):
        """Einstellungen"""
        
        st.subheader("⚙️ Einstellungen")
        
        # Blotato Config
        st.markdown("### 🔗 Blotato Konfiguration")
        
        blotato_key = st.text_input(
            "Blotato API Key",
            value=st.session_state.get('blotato_api_key', ''),
            type="password"
        )
        
        account_id = st.text_input("TikTok Account ID (aus Blotato)")
        
        if st.button("💾 Speichern"):
            st.session_state.blotato_api_key = blotato_key
            st.success("✅ Gespeichert!")
        
        # Backup/Export
        st.divider()
        st.markdown("### 💾 Datenbank")
        
        if st.button("📥 Daten exportieren (CSV)"):
            posts = self.db.get_all_posts()
            if posts:
                df = pd.DataFrame([
                    {
                        'id': p.id,
                        'pillar': p.content_pillar,
                        'hook': p.hook,
                        'caption': p.caption,
                        'status': p.status,
                        'created': p.created_at
                    }
                    for p in posts
                ])
                csv = df.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    csv,
                    "elternratgeber_posts.csv",
                    "text/csv"
                )


if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.run()
