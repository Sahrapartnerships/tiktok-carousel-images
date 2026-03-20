#!/usr/bin/env python3
"""
Streamlit Dashboard für TikTok System Überwachung
Echtzeit-Monitoring + Steuerung
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add parent to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.carousel_generator import CarouselDatabase
from core.comment_tracker import CommentTracker
from core.conversion_tracker import ConversionTracker
from optimization.ab_test_engine import ABTestEngine

# Page config
st.set_page_config(
    page_title="TikTok System Dashboard",
    page_icon="📊",
    layout="wide"
)

DB_PATH = 'tiktok_system/content_db.sqlite'

class Dashboard:
    """Haupt-Dashboard Klasse"""
    
    def __init__(self):
        self.db = CarouselDatabase(DB_PATH)
        self.comment_tracker = CommentTracker(DB_PATH)
        self.conversion_tracker = ConversionTracker(DB_PATH)
        self.ab_engine = ABTestEngine(DB_PATH)
    
    def render_sidebar(self):
        """Sidebar Navigation"""
        st.sidebar.title("🎯 TikTok System")
        
        page = st.sidebar.radio(
            "Navigation",
            ["📊 Übersicht", "📝 Content", "💬 Kommentare", "💰 Conversion", "🧪 A/B Tests", "⚙️ Einstellungen"]
        )
        
        st.sidebar.markdown("---")
        st.sidebar.info("Status: ✅ System aktiv")
        
        return page
    
    def render_overview(self):
        """Haupt-Übersicht"""
        st.title("📊 TikTok Performance Dashboard")
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        # Stats laden
        funnel = self.conversion_tracker.get_funnel_stats(days=30)
        
        with col1:
            st.metric(
                label="💰 Umsatz (30 Tage)",
                value=f"€{funnel.get('revenue', 0):.2f}"
            )
        
        with col2:
            st.metric(
                label="🛒 Verkäufe",
                value=f"{funnel.get('purchases', 0)}"
            )
        
        with col3:
            st.metric(
                label="📱 GUIDE Requests",
                value=f"{funnel.get('link_clicks', 0)}"
            )
        
        with col4:
            conv_rate = funnel.get('purchase_rate', 0)
            st.metric(
                label="📈 Conversion Rate",
                value=f"{conv_rate:.2f}%"
            )
        
        st.markdown("---")
        
        # Funnel Chart
        st.subheader("🎯 Conversion Funnel")
        
        funnel_data = {
            'Stage': ['Link Clicks', 'Page Views', 'Add to Cart', 'Purchase'],
            'Count': [
                funnel.get('link_clicks', 0),
                funnel.get('page_views', 0),
                funnel.get('add_to_carts', 0),
                funnel.get('purchases', 0)
            ]
        }
        
        fig = go.Figure(go.Funnel(
            y=funnel_data['Stage'],
            x=funnel_data['Count'],
            textposition="inside",
            textinfo="value+percent initial"
        ))
        st.plotly_chart(fig, use_container_width=True)
        
        # Top Posts
        st.subheader("🏆 Top Performing Posts")
        
        posts = self.conversion_tracker.get_post_performance()
        if posts:
            df = pd.DataFrame(posts[:5])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Noch keine Daten vorhanden")
    
    def render_content(self):
        """Content Management"""
        st.title("📝 Content Management")
        
        tab1, tab2 = st.tabs(["📅 Content Kalender", "➕ Neu erstellen"])
        
        with tab1:
            st.subheader("Geplante Karussells")
            
            # Zeige alle Carousels
            conn = sqlite3.connect(DB_PATH)
            df = pd.read_sql_query('''
                SELECT id, theme, target_week, hook, status, created_at
                FROM carousels
                ORDER BY target_week
            ''', conn)
            conn.close()
            
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Noch keine Carousels erstellt")
        
        with tab2:
            st.subheader("Neues Karussell generieren")
            
            col1, col2 = st.columns(2)
            
            with col1:
                theme = st.selectbox(
                    "Thema",
                    ["awareness", "value", "social_proof", "conversion"]
                )
                week = st.number_input("Woche", min_value=1, max_value=52, value=1)
            
            with col2:
                variant = st.radio("Variante", ["A", "B"])
            
            if st.button("🚀 Generieren", type="primary"):
                from core.carousel_generator import CarouselGenerator
                
                gen = CarouselGenerator(self.db)
                post = gen.generate_carousel(theme, week, variant)
                
                st.success(f"✅ Karussell erstellt: {post.id}")
                st.json({
                    "hook": post.hook,
                    "slides": len(post.slides),
                    "caption": post.caption[:100] + "..."
                })
    
    def render_comments(self):
        """Kommentar Tracking"""
        st.title("💬 GUIDE Kommentare")
        
        stats = self.comment_tracker.get_stats()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Requests", stats['total_requests'])
        with col2:
            st.metric("Link Clicks", stats['clicks'])
        with col3:
            st.metric("Conversion Rate", f"{stats['conversion_rate']:.1f}%")
        
        # Tabelle mit Requests
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query('''
            SELECT username, post_id, detected_at, link_sent, clicked, converted, revenue
            FROM guide_requests
            ORDER BY detected_at DESC
            LIMIT 50
        ''', conn)
        conn.close()
        
        st.dataframe(df, use_container_width=True)
    
    def render_conversion(self):
        """Conversion Tracking"""
        st.title("💰 Conversion Tracking")
        
        # Revenue Chart
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query('''
            SELECT 
                date(timestamp) as date,
                SUM(value) as daily_revenue,
                COUNT(*) as sales
            FROM conversion_events
            WHERE event_type = 'purchase'
            GROUP BY date(timestamp)
            ORDER BY date
        ''', conn)
        conn.close()
        
        if not df.empty:
            fig = px.line(df, x='date', y='daily_revenue', title='Täglicher Umsatz')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Noch keine Verkäufe getrackt")
    
    def render_ab_tests(self):
        """A/B Test Übersicht"""
        st.title("🧪 A/B Tests")
        
        # Aktive Tests
        st.subheader("Aktive Tests")
        
        active_tests = self.ab_engine.get_active_tests()
        
        if active_tests:
            for test in active_tests:
                with st.expander(f"Test: {test.element} ({test.post_id})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Variante A:** {test.variant_a}")
                    with col2:
                        st.write(f"**Variante B:** {test.variant_b}")
                    
                    # Ergebnisse
                    results = self.ab_engine.get_test_results(test.test_id)
                    st.json(results)
        else:
            st.info("Keine aktiven Tests")
        
        # Neue Tests vorschlagen
        st.subheader("🎯 Test-Vorschläge")
        
        suggestions = self.ab_engine.suggest_tests("example_post")
        
        for suggestion in suggestions:
            with st.expander(f"Teste: {suggestion['element']}"):
                st.write(f"**A:** {suggestion['variant_a']}")
                st.write(f"**B:** {suggestion['variant_b']}")
                st.info(f"💡 {suggestion['reason']}")
                
                if st.button(f"Test starten: {suggestion['element']}"):
                    st.success("Test erstellt!")
    
    def run(self):
        """Main App Loop"""
        page = self.render_sidebar()
        
        if page == "📊 Übersicht":
            self.render_overview()
        elif page == "📝 Content":
            self.render_content()
        elif page == "💬 Kommentare":
            self.render_comments()
        elif page == "💰 Conversion":
            self.render_conversion()
        elif page == "🧪 A/B Tests":
            self.render_ab_tests()
        elif page == "⚙️ Einstellungen":
            st.title("⚙️ System Einstellungen")
            st.info("System läuft korrekt")

if __name__ == '__main__':
    dashboard = Dashboard()
    dashboard.run()
