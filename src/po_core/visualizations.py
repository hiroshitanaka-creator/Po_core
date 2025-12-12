"""
Po_core Visualizations Module

Advanced visualization capabilities for Po_core including:
- Tension maps (heatmaps)
- Metrics timelines
- Philosopher interaction networks
- Export to PNG/SVG/HTML formats
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import json

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
import numpy as np
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from po_core.po_trace import PoTrace, Session


class PoVisualizer:
    """Advanced visualization system for Po_core.

    Provides graphical visualizations of philosophical reasoning
    including tension maps, metrics timelines, and interaction networks.
    """

    def __init__(self, po_trace: Optional[PoTrace] = None):
        """Initialize visualizer with optional PoTrace instance.

        Args:
            po_trace: PoTrace instance to use. If None, creates new instance.
        """
        self.po_trace = po_trace or PoTrace()

        # Set matplotlib style
        plt.style.use('seaborn-v0_8-darkgrid')

        # Color scheme for philosophers
        self.philosopher_colors = {
            'aristotle': '#8B4513',
            'sartre': '#DC143C',
            'heidegger': '#2F4F4F',
            'nietzsche': '#8B008B',
            'derrida': '#FF8C00',
            'wittgenstein': '#4682B4',
            'jung': '#9370DB',
            'dewey': '#228B22',
            'deleuze': '#FF6347',
            'kierkegaard': '#4B0082',
            'lacan': '#8B0000',
            'levinas': '#DAA520',
            'badiou': '#CD5C5C',
            'peirce': '#2E8B57',
            'merleau_ponty': '#6B8E23',
            'arendt': '#BC8F8F',
            'watsuji': '#B8860B',
            'wabi_sabi': '#D2B48C',
            'confucius': '#CD853F',
            'zhuangzi': '#8FBC8F',
        }

    def create_tension_map(
        self,
        session_id: str,
        output_path: Optional[Path] = None,
        format: str = 'png',
        figsize: Tuple[int, int] = (12, 8)
    ) -> Optional[Figure]:
        """Create tension map visualization showing philosophical tensions.

        Args:
            session_id: Session ID to visualize
            output_path: Path to save the figure. If None, returns figure without saving.
            format: Output format ('png', 'svg', 'pdf')
            figsize: Figure size as (width, height)

        Returns:
            matplotlib Figure if output_path is None, otherwise None
        """
        session = self.po_trace.get_session(session_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found")

        # Extract philosopher events with metrics
        philosopher_data = []
        for event in session.events:
            if 'philosopher' in event.data:
                philosopher_data.append({
                    'name': event.data['philosopher'],
                    'freedom_pressure': event.data.get('freedom_pressure', 0.0),
                    'semantic_delta': event.data.get('semantic_delta', 0.0),
                    'blocked_tensor': event.data.get('blocked_tensor', 0.0),
                })

        if not philosopher_data:
            raise ValueError(f"No philosopher data found in session {session_id}")

        # Create tension matrix
        philosophers = [p['name'] for p in philosopher_data]
        metrics = ['Freedom\nPressure', 'Semantic\nDelta', 'Blocked\nTensor']

        tension_matrix = np.array([
            [p['freedom_pressure'] for p in philosopher_data],
            [p['semantic_delta'] for p in philosopher_data],
            [p['blocked_tensor'] for p in philosopher_data],
        ])

        # Create figure
        fig, ax = plt.subplots(figsize=figsize)

        # Create heatmap
        im = ax.imshow(tension_matrix, cmap='YlOrRd', aspect='auto', vmin=0, vmax=1)

        # Set ticks and labels
        ax.set_xticks(np.arange(len(philosophers)))
        ax.set_yticks(np.arange(len(metrics)))
        ax.set_xticklabels(philosophers, rotation=45, ha='right')
        ax.set_yticklabels(metrics)

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Tension Level', rotation=270, labelpad=20)

        # Add values to cells
        for i in range(len(metrics)):
            for j in range(len(philosophers)):
                text = ax.text(j, i, f'{tension_matrix[i, j]:.2f}',
                             ha="center", va="center", color="black",
                             fontsize=9, weight='bold')

        # Title and labels
        prompt_short = session.prompt[:60] + '...' if len(session.prompt) > 60 else session.prompt
        ax.set_title(f'Philosophical Tension Map\n"{prompt_short}"',
                     fontsize=14, weight='bold', pad=20)
        ax.set_xlabel('Philosophers', fontsize=12, weight='bold')
        ax.set_ylabel('Tension Metrics', fontsize=12, weight='bold')

        # Add session info
        fig.text(0.99, 0.01, f'Session: {session_id[:12]}...',
                ha='right', fontsize=8, style='italic', alpha=0.6)

        plt.tight_layout()

        # Save or return
        if output_path:
            plt.savefig(output_path, format=format, dpi=300, bbox_inches='tight')
            plt.close()
            return None
        else:
            return fig

    def create_metrics_timeline(
        self,
        session_ids: List[str],
        output_path: Optional[Path] = None,
        format: str = 'html',
        title: Optional[str] = None
    ) -> Optional[go.Figure]:
        """Create interactive metrics timeline across multiple sessions.

        Args:
            session_ids: List of session IDs to visualize
            output_path: Path to save the figure. If None, returns figure.
            format: Output format ('html', 'png', 'svg')
            title: Custom title for the plot

        Returns:
            plotly Figure if output_path is None, otherwise None
        """
        if not session_ids:
            raise ValueError("At least one session ID required")

        # Collect metrics from all sessions
        timeline_data = []
        for session_id in session_ids:
            session = self.po_trace.get_session(session_id)
            if session is None:
                continue

            timeline_data.append({
                'session_id': session_id,
                'timestamp': session.created_at,
                'prompt': session.prompt[:40] + '...' if len(session.prompt) > 40 else session.prompt,
                **session.metrics
            })

        if not timeline_data:
            raise ValueError("No valid sessions found")

        # Create figure with subplots
        metrics_keys = list(timeline_data[0].keys())
        metrics_keys = [k for k in metrics_keys if k not in ['session_id', 'timestamp', 'prompt']]

        fig = make_subplots(
            rows=len(metrics_keys),
            cols=1,
            subplot_titles=[k.replace('_', ' ').title() for k in metrics_keys],
            vertical_spacing=0.08
        )

        # Add traces for each metric
        for idx, metric in enumerate(metrics_keys, 1):
            values = [d.get(metric, 0) for d in timeline_data]
            session_labels = [d['session_id'][:8] + '...' for d in timeline_data]
            hover_text = [
                f"Session: {d['session_id'][:12]}...<br>"
                f"Prompt: {d['prompt']}<br>"
                f"{metric}: {d.get(metric, 0):.3f}<br>"
                f"Time: {d['timestamp']}"
                for d in timeline_data
            ]

            fig.add_trace(
                go.Scatter(
                    x=list(range(len(timeline_data))),
                    y=values,
                    mode='lines+markers',
                    name=metric.replace('_', ' ').title(),
                    text=hover_text,
                    hovertemplate='%{text}<extra></extra>',
                    marker=dict(size=10),
                    line=dict(width=3)
                ),
                row=idx,
                col=1
            )

            # Update axis labels
            fig.update_xaxes(
                title_text="Session" if idx == len(metrics_keys) else "",
                ticktext=session_labels,
                tickvals=list(range(len(timeline_data))),
                row=idx,
                col=1
            )
            fig.update_yaxes(
                title_text="Value",
                range=[0, 1],
                row=idx,
                col=1
            )

        # Update layout
        plot_title = title or f"Metrics Timeline - {len(session_ids)} Sessions"
        fig.update_layout(
            title_text=plot_title,
            title_font_size=20,
            showlegend=False,
            height=300 * len(metrics_keys),
            hovermode='closest'
        )

        # Save or return
        if output_path:
            if format == 'html':
                fig.write_html(str(output_path))
            elif format == 'png':
                fig.write_image(str(output_path), format='png')
            elif format == 'svg':
                fig.write_image(str(output_path), format='svg')
            return None
        else:
            return fig

    def create_philosopher_network(
        self,
        session_id: str,
        output_path: Optional[Path] = None,
        format: str = 'png',
        figsize: Tuple[int, int] = (14, 10)
    ) -> Optional[Figure]:
        """Create philosopher interaction network graph.

        Shows relationships between philosophers based on their
        tension field interactions and semantic similarities.

        Args:
            session_id: Session ID to visualize
            output_path: Path to save the figure. If None, returns figure.
            format: Output format ('png', 'svg', 'pdf')
            figsize: Figure size as (width, height)

        Returns:
            matplotlib Figure if output_path is None, otherwise None
        """
        session = self.po_trace.get_session(session_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found")

        # Extract philosopher data
        philosopher_data = {}
        for event in session.events:
            if 'philosopher' in event.data:
                name = event.data['philosopher']
                philosopher_data[name] = {
                    'freedom_pressure': event.data.get('freedom_pressure', 0.0),
                    'semantic_delta': event.data.get('semantic_delta', 0.0),
                    'blocked_tensor': event.data.get('blocked_tensor', 0.0),
                }

        if len(philosopher_data) < 2:
            raise ValueError(f"Need at least 2 philosophers for network graph")

        # Create network graph
        G = nx.Graph()

        # Add nodes
        for name, data in philosopher_data.items():
            G.add_node(name, **data)

        # Add edges based on metric similarity
        philosophers = list(philosopher_data.keys())
        for i, phil1 in enumerate(philosophers):
            for phil2 in philosophers[i+1:]:
                # Calculate similarity (inverse of distance)
                d1 = philosopher_data[phil1]
                d2 = philosopher_data[phil2]

                distance = np.sqrt(
                    (d1['freedom_pressure'] - d2['freedom_pressure'])**2 +
                    (d1['semantic_delta'] - d2['semantic_delta'])**2 +
                    (d1['blocked_tensor'] - d2['blocked_tensor'])**2
                )

                similarity = 1 - min(distance / np.sqrt(3), 1.0)

                # Add edge if similarity is significant
                if similarity > 0.3:
                    G.add_edge(phil1, phil2, weight=similarity)

        # Create figure
        fig, ax = plt.subplots(figsize=figsize)

        # Layout
        pos = nx.spring_layout(G, k=2, iterations=50)

        # Draw nodes
        node_sizes = [
            (data['freedom_pressure'] + data['semantic_delta']) * 2000
            for _, data in philosopher_data.items()
        ]
        node_colors = [
            self.philosopher_colors.get(name.lower(), '#808080')
            for name in philosophers
        ]

        nx.draw_networkx_nodes(
            G, pos, ax=ax,
            node_size=node_sizes,
            node_color=node_colors,
            alpha=0.8,
            edgecolors='black',
            linewidths=2
        )

        # Draw edges
        edges = G.edges()
        weights = [G[u][v]['weight'] for u, v in edges]
        nx.draw_networkx_edges(
            G, pos, ax=ax,
            width=[w * 4 for w in weights],
            alpha=0.5,
            edge_color=weights,
            edge_cmap=plt.cm.Blues
        )

        # Draw labels
        nx.draw_networkx_labels(
            G, pos, ax=ax,
            font_size=10,
            font_weight='bold',
            font_color='white'
        )

        # Title
        prompt_short = session.prompt[:60] + '...' if len(session.prompt) > 60 else session.prompt
        ax.set_title(
            f'Philosopher Interaction Network\n"{prompt_short}"',
            fontsize=14,
            weight='bold',
            pad=20
        )

        # Legend
        legend_elements = [
            mpatches.Patch(facecolor=self.philosopher_colors.get(name.lower(), '#808080'),
                          edgecolor='black', label=name)
            for name in philosophers
        ]
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))

        # Add info
        ax.text(0.02, 0.02,
               f'Node size: Freedom Pressure + Semantic Delta\n'
               f'Edge width: Philosophical similarity\n'
               f'Session: {session_id[:12]}...',
               transform=ax.transAxes,
               fontsize=8,
               verticalalignment='bottom',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        ax.axis('off')
        plt.tight_layout()

        # Save or return
        if output_path:
            plt.savefig(output_path, format=format, dpi=300, bbox_inches='tight')
            plt.close()
            return None
        else:
            return fig

    def create_comprehensive_dashboard(
        self,
        session_id: str,
        output_path: Optional[Path] = None,
        format: str = 'html'
    ) -> Optional[go.Figure]:
        """Create comprehensive interactive dashboard for a session.

        Combines multiple visualizations into a single dashboard.

        Args:
            session_id: Session ID to visualize
            output_path: Path to save the dashboard
            format: Output format ('html' or 'png')

        Returns:
            plotly Figure if output_path is None, otherwise None
        """
        session = self.po_trace.get_session(session_id)
        if session is None:
            raise ValueError(f"Session {session_id} not found")

        # Extract data
        philosopher_data = []
        for event in session.events:
            if 'philosopher' in event.data:
                philosopher_data.append({
                    'name': event.data['philosopher'],
                    'freedom_pressure': event.data.get('freedom_pressure', 0.0),
                    'semantic_delta': event.data.get('semantic_delta', 0.0),
                    'blocked_tensor': event.data.get('blocked_tensor', 0.0),
                })

        if not philosopher_data:
            raise ValueError(f"No philosopher data in session {session_id}")

        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Tension Metrics by Philosopher',
                'Freedom Pressure Distribution',
                'Semantic vs Freedom Pressure',
                'Philosopher Contributions'
            ),
            specs=[
                [{'type': 'bar'}, {'type': 'box'}],
                [{'type': 'scatter'}, {'type': 'pie'}]
            ]
        )

        # 1. Bar chart - Tension metrics
        philosophers = [p['name'] for p in philosopher_data]
        fig.add_trace(
            go.Bar(name='Freedom Pressure',
                  x=philosophers,
                  y=[p['freedom_pressure'] for p in philosopher_data],
                  marker_color='indianred'),
            row=1, col=1
        )
        fig.add_trace(
            go.Bar(name='Semantic Delta',
                  x=philosophers,
                  y=[p['semantic_delta'] for p in philosopher_data],
                  marker_color='lightsalmon'),
            row=1, col=1
        )
        fig.add_trace(
            go.Bar(name='Blocked Tensor',
                  x=philosophers,
                  y=[p['blocked_tensor'] for p in philosopher_data],
                  marker_color='lightblue'),
            row=1, col=1
        )

        # 2. Box plot - Freedom pressure distribution
        fig.add_trace(
            go.Box(y=[p['freedom_pressure'] for p in philosopher_data],
                  name='Freedom Pressure',
                  marker_color='indianred'),
            row=1, col=2
        )

        # 3. Scatter plot - Semantic vs Freedom
        fig.add_trace(
            go.Scatter(
                x=[p['freedom_pressure'] for p in philosopher_data],
                y=[p['semantic_delta'] for p in philosopher_data],
                mode='markers+text',
                text=philosophers,
                textposition='top center',
                marker=dict(size=15, color='darkblue'),
                name='Philosophers'
            ),
            row=2, col=1
        )

        # 4. Pie chart - Philosopher contributions
        contributions = [p['freedom_pressure'] + p['semantic_delta'] for p in philosopher_data]
        fig.add_trace(
            go.Pie(labels=philosophers, values=contributions, name='Contribution'),
            row=2, col=2
        )

        # Update layout
        prompt_short = session.prompt[:60] + '...' if len(session.prompt) > 60 else session.prompt
        fig.update_layout(
            title_text=f'Po_core Session Dashboard<br><sub>"{prompt_short}"</sub>',
            title_font_size=20,
            showlegend=True,
            height=800,
            hovermode='closest'
        )

        # Save or return
        if output_path:
            if format == 'html':
                fig.write_html(str(output_path))
            elif format == 'png':
                fig.write_image(str(output_path), format='png', width=1400, height=800)
            return None
        else:
            return fig

    def export_session_visualizations(
        self,
        session_id: str,
        output_dir: Path,
        formats: List[str] = ['png', 'html']
    ) -> Dict[str, Path]:
        """Export all visualizations for a session.

        Args:
            session_id: Session ID to visualize
            output_dir: Directory to save visualizations
            formats: List of output formats ('png', 'svg', 'html')

        Returns:
            Dictionary mapping visualization name to output path
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        results = {}

        # Tension map
        for fmt in formats:
            if fmt in ['png', 'svg', 'pdf']:
                output_path = output_dir / f'tension_map_{session_id[:8]}.{fmt}'
                self.create_tension_map(session_id, output_path, format=fmt)
                results[f'tension_map_{fmt}'] = output_path

        # Philosopher network
        for fmt in formats:
            if fmt in ['png', 'svg', 'pdf']:
                output_path = output_dir / f'network_{session_id[:8]}.{fmt}'
                try:
                    self.create_philosopher_network(session_id, output_path, format=fmt)
                    results[f'network_{fmt}'] = output_path
                except ValueError:
                    # Skip if not enough philosophers
                    pass

        # Dashboard
        if 'html' in formats or 'png' in formats:
            fmt = 'html' if 'html' in formats else 'png'
            output_path = output_dir / f'dashboard_{session_id[:8]}.{fmt}'
            try:
                self.create_comprehensive_dashboard(session_id, output_path, format=fmt)
                results[f'dashboard_{fmt}'] = output_path
            except ValueError:
                pass

        return results
