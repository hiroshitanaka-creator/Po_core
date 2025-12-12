"""
Po_core Mock Philosopher System

Provides deterministic philosopher responses without requiring LLM APIs.
Useful for testing, development, and demonstrations.
"""
from typing import Dict, List, Optional
import random


class MockPhilosopher:
    """Base mock philosopher that returns deterministic responses."""

    def __init__(self, name: str, perspective: str):
        self.name = name
        self.perspective = perspective

        # Deterministic metrics for this philosopher
        random.seed(hash(name))
        self.base_freedom_pressure = random.uniform(0.6, 0.9)
        self.base_semantic_delta = random.uniform(0.4, 0.8)
        self.base_blocked_tensor = random.uniform(0.2, 0.5)

    def generate_response(self, prompt: str) -> Dict:
        """Generate a mock response to the prompt."""
        # Deterministic variation based on prompt
        prompt_hash = hash(prompt) % 100 / 100.0

        return {
            "philosopher": self.name,
            "perspective": self.perspective,
            "response": f"{self.name}'s perspective on: {prompt[:50]}...",
            "freedom_pressure": min(1.0, self.base_freedom_pressure + prompt_hash * 0.1),
            "semantic_delta": min(1.0, self.base_semantic_delta + prompt_hash * 0.15),
            "blocked_tensor": max(0.0, self.base_blocked_tensor - prompt_hash * 0.1),
        }


class MockPoSelf:
    """Mock version of Po_self that doesn't require LLM APIs."""

    def __init__(self, enable_trace: bool = True):
        """Initialize mock Po_self with predefined philosophers."""
        from po_core.po_trace import PoTrace, EventType

        self.enable_trace = enable_trace
        self.po_trace = PoTrace() if enable_trace else None

        # Create mock philosophers
        self.philosophers = {
            "aristotle": MockPhilosopher("Aristotle", "Virtue Ethics"),
            "nietzsche": MockPhilosopher("Nietzsche", "Will to Power"),
            "sartre": MockPhilosopher("Sartre", "Existential Freedom"),
            "heidegger": MockPhilosopher("Heidegger", "Being and Dasein"),
            "derrida": MockPhilosopher("Derrida", "Deconstruction"),
            "wittgenstein": MockPhilosopher("Wittgenstein", "Language Games"),
            "jung": MockPhilosopher("Jung", "Collective Unconscious"),
            "dewey": MockPhilosopher("Dewey", "Pragmatism"),
            "deleuze": MockPhilosopher("Deleuze", "Difference and Repetition"),
            "kierkegaard": MockPhilosopher("Kierkegaard", "Subjective Truth"),
            "lacan": MockPhilosopher("Lacan", "Psychoanalysis"),
            "levinas": MockPhilosopher("Levinas", "Ethics of the Other"),
            "badiou": MockPhilosopher("Badiou", "Event and Truth"),
            "peirce": MockPhilosopher("Peirce", "Semiotics"),
            "merleau_ponty": MockPhilosopher("Merleau-Ponty", "Phenomenology of Perception"),
            "arendt": MockPhilosopher("Arendt", "Political Action"),
            "watsuji": MockPhilosopher("Watsuji", "Betweenness"),
            "wabi_sabi": MockPhilosopher("Wabi-Sabi", "Imperfection"),
            "confucius": MockPhilosopher("Confucius", "Humaneness"),
            "zhuangzi": MockPhilosopher("Zhuangzi", "Natural Spontaneity"),
        }

    def generate(
        self,
        prompt: str,
        philosophers: Optional[List[str]] = None
    ) -> Dict:
        """Generate mock philosophical response.

        Args:
            prompt: The question or prompt
            philosophers: List of philosopher names to use (default: random 3-5)

        Returns:
            Dictionary with response and metadata
        """
        from po_core.po_trace import EventType

        # Select philosophers
        if philosophers is None:
            num_philosophers = random.randint(3, 5)
            selected = random.sample(list(self.philosophers.keys()), num_philosophers)
        else:
            selected = [p.lower().replace(" ", "_") for p in philosophers]
            selected = [p for p in selected if p in self.philosophers]

        if not selected:
            selected = ["aristotle", "nietzsche", "sartre"]

        # Create session
        session_id = None
        if self.enable_trace:
            session_id = self.po_trace.create_session(
                prompt=prompt,
                philosophers=selected
            )

            # Log start event
            self.po_trace.log_event(
                session_id=session_id,
                event_type=EventType.EXECUTION,
                source="ensemble",
                data={"message": "Mock ensemble started"}
            )

        # Generate responses from each philosopher
        responses = []
        total_fp = 0.0
        total_sd = 0.0
        total_bt = 0.0

        for phil_name in selected:
            philosopher = self.philosophers[phil_name]
            response = philosopher.generate_response(prompt)
            responses.append(response)

            total_fp += response["freedom_pressure"]
            total_sd += response["semantic_delta"]
            total_bt += response["blocked_tensor"]

            # Log philosopher event
            if self.enable_trace:
                self.po_trace.log_event(
                    session_id=session_id,
                    event_type=EventType.EXECUTION,
                    source=f"philosopher.{response['philosopher']}",
                    data={
                        "message": f"{response['philosopher']} completed",
                        "philosopher": response["philosopher"],
                        "freedom_pressure": response["freedom_pressure"],
                        "semantic_delta": response["semantic_delta"],
                        "blocked_tensor": response["blocked_tensor"],
                        "perspective": response["perspective"],
                    }
                )

        # Calculate ensemble metrics
        n = len(responses)
        avg_fp = total_fp / n
        avg_sd = total_sd / n
        avg_bt = total_bt / n

        # Update session metrics
        if self.enable_trace:
            self.po_trace.update_metrics(
                session_id,
                {
                    "freedom_pressure": avg_fp,
                    "semantic_delta": avg_sd,
                    "blocked_tensor": avg_bt,
                }
            )

        # Generate synthetic ensemble response
        ensemble_response = (
            f"After considering perspectives from {', '.join([r['philosopher'] for r in responses])}, "
            f"the philosophical ensemble suggests: [Mock response to: {prompt}]\n\n"
            f"Key tensions: Freedom Pressure={avg_fp:.2f}, "
            f"Semantic Delta={avg_sd:.2f}, Blocked Tensor={avg_bt:.2f}"
        )

        return {
            "text": ensemble_response,
            "freedom_pressure": avg_fp,
            "semantic_delta": avg_sd,
            "blocked_tensor": avg_bt,
            "philosophers_involved": selected,
            "log": {
                "session_id": session_id,
                "philosopher_responses": responses,
            }
        }


# Convenience function
def create_mock_sessions(
    prompts: List[str],
    philosophers_per_session: Optional[int] = None
) -> List[str]:
    """Create multiple mock sessions for testing.

    Args:
        prompts: List of prompts to generate sessions for
        philosophers_per_session: Number of philosophers per session (default: random 3-5)

    Returns:
        List of session IDs
    """
    mock_po = MockPoSelf(enable_trace=True)
    session_ids = []

    for prompt in prompts:
        if philosophers_per_session:
            phil_names = random.sample(
                list(mock_po.philosophers.keys()),
                philosophers_per_session
            )
            result = mock_po.generate(prompt, philosophers=phil_names)
        else:
            result = mock_po.generate(prompt)

        session_ids.append(result["log"]["session_id"])

    return session_ids, mock_po.po_trace
