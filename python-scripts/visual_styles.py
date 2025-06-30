"""
Visual Style Templates for Image Generation
Based on the comprehensive style guide provided
"""

class VisualStyleTemplates:
    """
    Six main visual style templates with formulas and characteristics
    """
    
    HIGH_CONTRAST = {
        "name": "High Contrast and Vivid Colors",
        "formula": "[Bold subject + Vibrant color palette + Simple/neutral background + Sharp lighting]",
        "elements": {
            "bold_subject": {
                "description": "Central figure or object must be simple yet striking",
                "examples": ["tiger", "soda can", "motorbike helmet", "screaming face", "giant strawberry"]
            },
            "vibrant_colors": {
                "description": "High-saturation and complementary colors",
                "examples": ["neon pink vs cyan", "red vs yellow", "electric blue", "lime green", "magenta"]
            },
            "simple_background": {
                "description": "Keeps attention on subject by removing visual noise",
                "examples": ["black", "white", "gradient grey", "soft shadow", "radial light flare"]
            },
            "sharp_lighting": {
                "description": "Hard shadows or glowing edges enhance contrast",
                "examples": ["rim light", "spotlight from above", "backlight silhouette", "neon underglow", "dual-tone shadow"]
            }
        },
        "prompt_examples": [
            "Neon tiger face glowing in black background, cyan and magenta, hyper sharp lighting",
            "High-contrast soda can, red vs yellow, flat grey backdrop",
            "Portrait of dancer under neon lights, electric blue and pink highlight",
            "Futuristic motorcycle helmet, lime green and black, spotlight focus",
            "Magenta skull surrounded by glowing wires on dark background"
        ]
    }
    
    INCONGRUOUS_ELEMENTS = {
        "name": "Unusual or Incongruous Element Combinations",
        "formula": "[Familiar object + Surreal twist + Dreamlike or abstract context]",
        "elements": {
            "familiar_object": {
                "description": "Common things to ground viewer before subverting expectations",
                "examples": ["teacup", "astronaut", "goldfish", "apple", "vintage camera"]
            },
            "surreal_twist": {
                "description": "Feature or transformation that breaks logic or physics",
                "examples": ["floating", "melting", "inside-out", "replaced parts", "unexpected texture"]
            },
            "dreamlike_context": {
                "description": "Illogical space that feels like a dream or hallucination",
                "examples": ["cloud ocean", "desert sky", "infinite mirror room", "upside-down house", "pastel void"]
            }
        },
        "prompt_examples": [
            "Goldfish flying through a cloudy sky, soft light, dreamlike",
            "Teacup filled with stars and planets, on desert sand",
            "Apple with an eye in the center, floating in pastel space",
            "Astronaut swimming in coffee, abstract marble waves",
            "Melting camera resting on a chair made of clouds"
        ]
    }
    
    INTENSE_EYE_CONTACT = {
        "name": "Intense Eye Contact / Gaze",
        "formula": "[Central figure facing viewer + Emotive or glowing eyes + Tight crop or portrait focus + Minimal distraction]",
        "elements": {
            "central_figure": {
                "description": "Subject must directly engage viewer, centered in frame",
                "examples": ["girl", "owl", "lion", "child", "cyborg"]
            },
            "emotive_eyes": {
                "description": "Eyes carry emotion or enhanced visuals as focal point",
                "examples": ["glowing pupils", "tears", "animal shine", "cyber implants", "intense makeup"]
            },
            "tight_crop": {
                "description": "Close framing brings attention to face and emotion",
                "examples": ["head-and-shoulders view", "chin-up framing", "one-eye zoom", "symmetrical crop", "blurred edges"]
            },
            "minimal_distraction": {
                "description": "Background neutral, blurred, or abstract to isolate gaze",
                "examples": ["grey fog", "gradient blur", "solid black", "radial fade", "soft bokeh"]
            }
        },
        "prompt_examples": [
            "Close-up owl with golden glowing eyes, intense stare, blurred forest behind",
            "Girl staring into camera, cybernetic eyes glowing blue, dark gradient background",
            "Child's face crying with shimmering tears, tight frame, blurred edges",
            "Lion close-up, burning red eyes, smoky shadow background",
            "Cyborg portrait, glowing implant eyes, high-detail face, soft blur behind"
        ]
    }
    
    NEGATIVE_SPACE_MYSTERY = {
        "name": "Negative Space and Sense of Mystery",
        "formula": "[Minimal subject placement + Large negative space + Subtle emotion or hint + Limited color palette]",
        "elements": {
            "minimal_subject": {
                "description": "Small object or figure occupies tiny portion of composition",
                "examples": ["person standing", "floating balloon", "single door", "small shadow", "tiny boat"]
            },
            "large_negative_space": {
                "description": "Vast empty areas create mood and interpretive breathing room",
                "examples": ["blank sky", "white wall", "black void", "mist", "gradient fog"]
            },
            "subtle_emotion": {
                "description": "Subject suggests feeling but doesn't explicitly tell story",
                "examples": ["back turned", "slouched posture", "reaching gesture", "flickering light", "cracked surface"]
            },
            "limited_palette": {
                "description": "Use only 2-3 tones to maintain quiet atmosphere",
                "examples": ["white and grey", "soft blue", "beige and black", "muted pink", "dusty lavender"]
            }
        },
        "prompt_examples": [
            "A child stands in the fog, tiny figure in white void, silhouette only",
            "Small open door in an all-black room, warm light spills out",
            "Lone balloon drifting over a grey desert, wide empty sky",
            "Silhouette of person under soft snowfall, pale beige tones",
            "Tiny boat floating in endless pastel ocean, back-facing figure"
        ]
    }
    
    HAND_DRAWN_CHILDLIKE = {
        "name": "Hand-Drawn / Childlike Style",
        "formula": "[Simple shapes + Imperfect lines + Playful subject + Bright naive colors]",
        "elements": {
            "simple_shapes": {
                "description": "Characters or objects made of geometric and soft forms",
                "examples": ["circles", "triangles", "stick limbs", "cloud shapes", "oversized heads"]
            },
            "imperfect_lines": {
                "description": "Hand-drawn look with wobble, asymmetry, or childlike perspective",
                "examples": ["pencil sketch", "crayon stroke", "broken outline", "ink smudge", "uneven border"]
            },
            "playful_subject": {
                "description": "Joyful or silly characters/situations with friendly energy",
                "examples": ["smiling sun", "roller-skating dog", "hugging apples", "dancing cat", "rainbow tree"]
            },
            "bright_naive_colors": {
                "description": "Colors are flat, bold, sometimes go outside the lines",
                "examples": ["sky blue", "cherry red", "banana yellow", "crayon green", "candy pink"]
            }
        },
        "prompt_examples": [
            "Crayon drawing of a happy sun and rabbit flying on balloons",
            "Scribbled dinosaur holding a cupcake, on notebook paper",
            "Hand-drawn rainbow with dancing fruit characters",
            "Childlike sketch of a dog on a skateboard, yellow background",
            "Naive-style fish and cat playing together, soft pastels"
        ]
    }
    
    STYLE_CONTRAST_CUTE_CREEPY = {
        "name": "Style Contrast (Cute + Creepy)",
        "formula": "[Cute character base + Disturbing detail or twist + Contrasting palette + Mood conflict]",
        "elements": {
            "cute_character": {
                "description": "Rounded features, big eyes, soft forms (kawaii styles)",
                "examples": ["bunny", "plush bear", "anime girl", "tiny demon", "frog"]
            },
            "disturbing_detail": {
                "description": "Dark, creepy, or violent detail that disrupts innocence",
                "examples": ["cracked face", "stitched smile", "blood splatter", "blank stare", "third eye"]
            },
            "contrasting_palette": {
                "description": "Soft/candy tones juxtaposed with harsh/dark/bloody ones",
                "examples": ["pink and black", "lavender and red", "sky blue with deep shadows", "mint with crimson"]
            },
            "mood_conflict": {
                "description": "Creates discomfort from emotional dissonance",
                "examples": ["happy pose + haunted eyes", "soft lighting + violent gesture", "cute dress + scary aura"]
            }
        },
        "prompt_examples": [
            "Cute bunny with stitched smile, pink fur, holding a knife in soft light",
            "Kawaii ghost girl in school uniform, blank black eyes, candy-colored background",
            "Plush teddy bear covered in cracks, holding a lollipop with blood stains",
            "Smiling frog with glowing eyes, in a gothic candy world",
            "Childlike demon with flower crown, smiling in front of a burning village"
        ]
    }

class TextEffects:
    """Text effects and treatments for different visual styles"""
    
    EFFECTS = {
        "cartoon": {
            "keywords": "Rounded lines, vibrant colors",
            "description": "Adds fun and friendliness"
        },
        "3d": {
            "keywords": "Shadows, highlights, depth",
            "description": "Strong modern visual"
        },
        "glow": {
            "keywords": "Bright, neon, fluorescent",
            "description": "High visual impact"
        },
        "liquid": {
            "keywords": "Flowing, gradient, translucent",
            "description": "Dynamic and organic"
        },
        "metal": {
            "keywords": "Reflective, shiny, cold-toned",
            "description": "Hard-edged, textured"
        },
        "wood": {
            "keywords": "Grainy, earthy tones",
            "description": "Natural and retro"
        },
        "flame": {
            "keywords": "Fiery colors, burning dynamics",
            "description": "Intense and energetic"
        },
        "frost": {
            "keywords": "Crystals, frost textures",
            "description": "Cool-toned and 3D"
        },
        "ink_wash": {
            "keywords": "Ink smudges, calligraphic feel",
            "description": "Artistic and cultural"
        },
        "cracked": {
            "keywords": "Broken texture, rough surface",
            "description": "Worn-out and dramatic"
        },
        "embossed": {
            "keywords": "Light and shadow relief",
            "description": "Classical and elegant"
        },
        "blur": {
            "keywords": "Low contrast, dreamy",
            "description": "Soft and mystical"
        },
        "mirror": {
            "keywords": "Symmetrical reflection",
            "description": "Balanced and creative"
        },
        "gradient": {
            "keywords": "Color transition, rich layering",
            "description": "Visually appealing"
        },
        "glass": {
            "keywords": "Transparent, glossy, crystal-like",
            "description": "Light and refined"
        },
        "tech": {
            "keywords": "Glow, circuit textures",
            "description": "Futuristic and digital"
        }
    }

class VisualStyleSelector:
    """Helper class to select and generate style configurations"""
    
    @classmethod
    def get_all_styles(cls):
        """Get all available visual styles"""
        return {
            "high_contrast": VisualStyleTemplates.HIGH_CONTRAST,
            "incongruous": VisualStyleTemplates.INCONGRUOUS_ELEMENTS,
            "eye_contact": VisualStyleTemplates.INTENSE_EYE_CONTACT,
            "negative_space": VisualStyleTemplates.NEGATIVE_SPACE_MYSTERY,
            "hand_drawn": VisualStyleTemplates.HAND_DRAWN_CHILDLIKE,
            "cute_creepy": VisualStyleTemplates.STYLE_CONTRAST_CUTE_CREEPY
        }
    
    @classmethod
    def get_style(cls, style_name):
        """Get specific style by name"""
        styles = cls.get_all_styles()
        return styles.get(style_name)
    
    @classmethod
    def get_style_names(cls):
        """Get list of all style names"""
        return list(cls.get_all_styles().keys())
    
    @classmethod
    def build_style_prompt_elements(cls, style_name, subject, color_palette=None):
        """Build prompt elements based on style formula"""
        style = cls.get_style(style_name)
        if not style:
            return None
            
        elements = style["elements"]
        formula_parts = []
        
        # Extract formula components and build prompt
        if style_name == "high_contrast":
            formula_parts = [
                f"Bold {subject}",
                "vibrant color palette with high-saturation complementary colors",
                "simple neutral background",
                "sharp lighting with hard shadows"
            ]
        elif style_name == "incongruous":
            formula_parts = [
                f"Familiar {subject}",
                "with surreal twist that breaks logic",
                "in dreamlike abstract context"
            ]
        elif style_name == "eye_contact":
            formula_parts = [
                f"{subject} facing viewer directly",
                "with emotive glowing eyes as focal point",
                "tight portrait crop",
                "minimal distraction background"
            ]
        elif style_name == "negative_space":
            formula_parts = [
                f"Small {subject} in minimal placement",
                "large negative space creating mood",
                "subtle emotional hint",
                "limited 2-3 color palette"
            ]
        elif style_name == "hand_drawn":
            formula_parts = [
                f"Hand-drawn {subject} with simple shapes",
                "imperfect lines with childlike perspective",
                "playful joyful energy",
                "bright naive flat colors"
            ]
        elif style_name == "cute_creepy":
            formula_parts = [
                f"Cute {subject} with rounded kawaii features",
                "disturbing detail that disrupts innocence",
                "contrasting soft and harsh color palette",
                "mood conflict creating emotional dissonance"
            ]
            
        return {
            "style_name": style["name"],
            "formula": style["formula"],
            "prompt_elements": formula_parts,
            "example_prompts": style["prompt_examples"]
        }