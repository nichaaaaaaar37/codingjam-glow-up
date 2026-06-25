# UX Design Document: AI Hairstyle Try-On App

## 1. User Journey
The user journey is optimized for speed and the single magical moment. It consists of a simple two-step process: Upload & Select -> Reveal.

## 2. Screen-by-Screen Specs

### Screen 1: The Input Screen (Home)
* **Layout:** Centered, mobile-first design.
* **Components:**
  * **Hero Header:** "Find Your Next Vibe"
  * **Upload Area:** A large, inviting dropzone/button labeled "Upload Selfie".
  * **Preset Selector:** A horizontally scrollable row or a 2x2 grid of 4 distinct hairstyle presets (e.g., "The Bob", "Curtain Bangs", "Pixie Cut", "Beach Waves"). Each preset should be a highly visual, stylized icon or representative image.
  * **Action Button:** "Transform Me" (Disabled until a photo is uploaded and a preset is selected).

### Screen 2: The Reveal Screen (Result)
* **Layout:** Immersive, focus on the visual output.
* **Components:**
  * **The Comparison:** A side-by-side image layout displaying the original selfie and the generated hairstyle image. 
  * **The Signature Detail:** A prominent text banner beneath the images displaying the dynamic "vibe rating" or sassy stylist note (e.g., *Stylist says: "Serving 90s rom-com protagonist!"*).
  * **Action Button:** "Try Another Style" (Returns user to Screen 1).

## 3. Interaction Details & Edge States
* **Loading State:** When the user clicks "Transform Me", replace the button with a playful loading animation (e.g., a spinning pair of scissors or a hairdryer) and a message like "Consulting the AI stylist...". This builds anticipation for the magical moment.
* **Error State:** If the upload fails or no face is detected, show a friendly toast: "Oops, we couldn't see your face clearly. Try another selfie!"
* **Edge State:** User clicks "Transform Me" without selecting a preset. -> Slight shake animation on the preset grid to draw attention.

## 4. The Signature Interaction
The core defining interaction is the **Reveal**. The transition from the loading state to the final side-by-side comparison should be instant and crisp, making the "before and after" impact as dramatic as possible. No unnecessary animations should delay seeing the final image.
