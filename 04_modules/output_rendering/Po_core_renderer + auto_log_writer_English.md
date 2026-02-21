As an integrated solution, Po_core_renderer + auto_log_writer combines three key elements: structural design, behavior, and responsibility tensor alignment.

Imports:

json

argparse

datetime from datetime

os

Renderer
def render_po_core_output(data):
    print(f"\n 🧠 Po_core_output v{data['schema_version']} | Po_ID: {data['po_id']}")
    print(f"Prompt: {data['input_text']}")
    print(f"❌ Original Output: {data['output_text']}")
    print(f"✅ Final Output: {data['final_output']['text']}")
    print(f"Mist Flags: {', '.join(data['mist_flags'])}")
    print("\n🔧 Reconstruction Steps:")
    for step in data["reconstruction_steps"]:
        print(f" - [{step['step_id']}] {step['type']} | Tier: {step['importance_tier']} | Confidence: {step['confidence']}")
        if step.get("review_notes"):
            print(f"    🔍 Reason: {step['review_notes']}")
    print("\n📎 Validation:", data["responsibility_summary"].get("method_label", "?"))
    fb = data.get("user_feedback", {})
    if fb:
        print(f"📣 Feedback: {'Accepted' if fb.get('accepted') else 'Rejected'} | {fb.get('comment', '')}")
        if fb.get("suggested_rewrite"):
            print(f"✏️ Suggested Rewrite: {fb['suggested_rewrite']}")

Log Writer
def write_log(data, logdir="logs/"):
    os.makedirs(logdir, exist_ok=True)
    po_id = data.get("po_id", "po_output")
    fname = f"{po_id}_{datetime.utcnow().isoformat().replace(':', '-')}.json"
    fpath = os.path.join(logdir, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return fpath

CLI Entry
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Po_core_output JSON file")
    parser.add_argument("--mode", type=str, default="full", choices=["full", "compact"])
    parser.add_argument("--logdir", type=str, default="logs/", help="Directory to save output logs")
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Failed to read input: {e}")
        exit(1)

    if args.mode == "compact":
        print(f" 🧠 Po_ID: {data.get('po_id', '?')} | Final: {data['final_output']['text']} ")
    else:
        render_po_core_output(data)

    path = write_log(data, logdir=args.logdir)
    print(f"\n💾 Log saved to {path}")









