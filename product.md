# Product Requirements Document: AI Hairstyle Try-On App (MMV)

## 1. Goal & Context
To build an AI-powered hairstyle try-on application focused on a single magical moment: instant, realistic self-transformation. This is a Minimum Viable Magic (MMV) build, optimizing for speed to value and a delightful user experience over feature completeness.

## 2. The Magical Moment
**"OMG, that's me with bangs!"**
The core value proposition is the instant gratification of seeing a highly realistic, transformed version of oneself. Everything in the product should serve to make this moment fast, believable, and delightful.

## 3. Core Requirements (The Contract)
* **Input:**
  * User uploads a selfie image.
  * User selects one of four predefined hairstyle presets.
* **Output:**
  * A side-by-side "before and after" image comparison.
* **Signature Detail:**
  * Alongside the final output image, the user will receive a fun "vibe rating" or a sassy stylist note (e.g., "Serving 90s rom-com protagonist!").

## 4. Scope Discipline (What We Are NOT Building)
To maintain velocity and focus on the magical moment, the following are strictly **out of scope**:
* Outfits or wardrobe changes.
* Custom, user-typed text prompts for generation.
* Save, download, or share buttons (users can take screenshots if they want).
* Lookbooks, galleries, or user accounts/history.

## 5. Handoff to UX & Engineering
* **UX:** Focus on a frictionless upload flow, clear selection of the 4 presets, and a dramatic reveal for the side-by-side comparison and the sassy stylist note. Keep screens to an absolute minimum.
* **Engineering:** Optimize for latency in the image generation pipeline. The transformation must be realistic. Ensure the "vibe rating" generation is fast and reliable.
