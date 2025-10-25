SQUAT_CRITERIA = """
# Squat Exercise Guide

## Form Standard (Good Rep)

- Feet slightly wider than hip-width, toes pointed slightly outward.

- Sit the hips back and down as if lowering into a chair; knees track in line with toes.

- Lower until thighs are at least parallel to the ground (if mobility allows) while keeping weight distributed through heels and mid-foot.

- Maintain a neutral spine: chest up, back straight (not rounded or overly arched). Engage core.

- Rise by pushing through heels and mid-foot, hips and knees extending together. Reset posture before next rep.

## Common Errors and What to Look For

- **Knees collapsing inward (valgus) or drifting off over toes** — improper knee tracking.

- **Not sitting back (hips too forward) or weight shifting onto toes** — improper hip hinge.

- **Heels lifting off the ground** — poor weight distribution.

- **Rounding or arching the lower back** — lose neutral spine.

- **Chest dropping forward or head tilting down/up** — improper upper body position.

- **Depth too shallow (thighs above parallel)** — when mobility allows deeper.
"""

PUSHUP_CRITERIA = """
# Push-Up Exercise Guide

## Form Standard (Good Rep)

- Begin in a high plank position: hands slightly wider than shoulders, feet hip-width apart, body in a straight line from head to heels.

- Keep core engaged, glutes tight, shoulders recruited—avoid sagging hips or raised butt.

- Hands positioned directly under or just outside shoulders; wrists, elbows and shoulders aligned.

- Elbows should bend to approx 45° angle relative to torso (for many individuals) as you lower the body.

- Lower body until chest is just above floor (or until elbows approx 90°) while maintaining body line, then push back up through palms to full extension.

## Common Errors and What to Look For

- **Hips sagging toward the floor or raised too high (pike position)** — breaks straight line.

- **Elbows flaring out wide (>60°)** — can stress shoulders.

- **Hands too far forward or too wide from shoulders** — improper alignment.

- **Incomplete range of motion (too shallow)** — not lowering chest near floor.

- **Poor core/bracing** — resulting in arching back or letting belly drop.

- **Neck craning up or head dropping downward** — improper head position.
"""

CRITERIAS_MAP = {
    "squat": SQUAT_CRITERIA,
    "push_up": PUSHUP_CRITERIA
}