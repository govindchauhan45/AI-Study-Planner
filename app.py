import os
import json
import random
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory,redirect
import requests
from flask_cors import CORS

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-r1:free")

app = Flask(__name__)

# Enable CORS for all domains
CORS(app, origins="*")

@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "message": "AI Study Planner Backend (HuggingFace Space)"
    })

# ----------------------------------------------------
#  AI Assistant API
# ----------------------------------------------------
@app.route('/api/assistant', methods=['POST', 'OPTIONS'])
def assistant():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    try:
        data = request.get_json(force=True)
        prompt = data.get('prompt', '').strip()
        length_hint = float(data.get('length_hint', 1.0))
        
        if not prompt:
            return jsonify({"error": "Prompt required"}), 400

        if not OPENROUTER_API_KEY:
            return jsonify({"error": "No OPENROUTER_API_KEY set in environment"}), 500

        base_tokens = 500
        if length_hint <= 0.5:
            max_tokens = int(base_tokens * 0.5)
        elif length_hint >= 1.5:
            max_tokens = int(base_tokens * 2)
        else:
            max_tokens = base_tokens

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "Study Planner AI"
        }
        
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a helpful, concise study assistant."
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": max_tokens,
            "top_p": 0.9
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 429:
            return jsonify({
                "error": "API rate limit exceeded.",
                "retry_after": response.headers.get('Retry-After', '60')
            }), 429
            
        response.raise_for_status()
        
        result = response.json()
        text = result.get("choices", [{}])[0].get("message", {}).get("content", "No response received")
        
        return jsonify({"text": text, "model_used": OPENROUTER_MODEL})
        
    except requests.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


# ----------------------------------------------------
#  MUSIC API WITH SPOTIFY + YOUTUBE SUPPORT
# ----------------------------------------------------
@app.route('/api/music-suggest', methods=['POST', 'OPTIONS'])
def music_suggest():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    try:
        data = request.get_json(force=True)
        mood = data.get('mood', 'calm').lower()
        language = data.get('language', 'english').lower()
        ptype = data.get('ptype', 'lofi').lower()

        # ----------------------------------------------------
        #  FULL SPOTIFY + YOUTUBE PLAYLIST DATABASE
        # ----------------------------------------------------
        playlists = {
            "focused": {
                "english": {
                    "lofi": {
                        "youtube": "https://www.youtube.com/embed/jfKfPfyJRdk?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX8Uebhn9wzrS",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/37i9dQZF1DX8Uebhn9wzrS"
                    },
                    "pop": {
                        "youtube": "https://www.youtube.com/embed/y6120QOlsfU?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX4UtSsGT1Sbe",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/37i9dQZF1DX4UtSsGT1Sbe"
                    },
                    "melody": {
                        "youtube": "https://www.youtube.com/embed/5yx6BWlEVcY?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DWZd79rJ6a7lp",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/37i9dQZF1DWZd79rJ6a7lp"
                    },
                    "beats": {
                        "youtube": "https://www.youtube.com/embed/36YnV9STBqc?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX4o1oenSJRJd",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/37i9dQZF1DX4o1oenSJRJd"
                    }
                },
"tamil": {
                    "lofi": {
                        "youtube": "https://www.youtube.com/embed/MGQ5m0QdCjE?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/1E1j2PbaSW1byDCxtaiGlg",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/1E1j2PbaSW1byDCxtaiGlg"
                    },
                    "pop": {
                        "youtube": "https://www.youtube.com/embed/r00ikilDxW4?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DXaVmfUr97Uve",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/37i9dQZF1DXaVmfUr97Uve"
                    },
                    "melody": {
                        "youtube": "https://www.youtube.com/embed/HpEi0lrpLDo?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/4zzmGEbnAkLZRiVO9b9eGO",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/4zzmGEbnAkLZRiVO9b9eGO"
                    },
                    "beats": {
                        "youtube": "https://www.youtube.com/embed/1q8gp2AB6VY?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/43a73ssTnlw00K8ljXDEfO",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/43a73ssTnlw00K8ljXDEfO"
                    }
                }
            },

            # ----------------------------------------------------
            #  CALM
            # ----------------------------------------------------
            "calm": {
                "english": {
                    "lofi": {
                        "youtube": "https://www.youtube.com/embed/5yx6BWlEVcY?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/1DWuFSxuyo6xjLsanCwGTC",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/1DWuFSxuyo6xjLsanCwGTC"
                    },
                    "pop": {
                        "youtube": "https://www.youtube.com/embed/EkHTsc9PU2A?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/37i9dQZF1DX3rxVfibe1L0"
                    },
                    "melody": {
                        "youtube": "https://www.youtube.com/embed/1ZYbU82GVz4?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DWXmlLSKkfdAk",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/37i9dQZF1DWXmlLSKkfdAk"
                    },
                    "beats": {
                        "youtube": "https://www.youtube.com/embed/2OEL4P1Rz04?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX6VdMW310YC7",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/37i9dQZF1DX6VdMW310YC7"
                    }
                },

"tamil": {
                    "lofi": {
                        "youtube": "https://www.youtube.com/embed/MGQ5m0QdCjE?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/1E1j2PbaSW1byDCxtaiGlg",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/1E1j2PbaSW1byDCxtaiGlg"
                    },
                    "pop": {
                        "youtube": "https://www.youtube.com/embed/r00ikilDxW4?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DXaVmfUr97Uve",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/37i9dQZF1DXaVmfUr97Uve"
                    },
                    "melody": {
                        "youtube": "https://www.youtube.com/embed/HpEi0lrpLDo?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/4zzmGEbnAkLZRiVO9b9eGO",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/4zzmGEbnAkLZRiVO9b9eGO"
                    },
                    "beats": {
                        "youtube": "https://www.youtube.com/embed/1q8gp2AB6VY?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/43a73ssTnlw00K8ljXDEfO",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/43a73ssTnlw00K8ljXDEfO"
                    }
                }
            },

            # ----------------------------------------------------
            #  ENERGETIC
            # ----------------------------------------------------
            "energetic": {
                "english": {
                    "lofi": {
                        "youtube": "https://www.youtube.com/embed/hi4pzKvuEQM?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX76Wlfdnj7AP",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/37i9dQZF1DX76Wlfdnj7AP"
                    },
                    "pop": {
                        "youtube": "https://www.youtube.com/embed/kXYiU_JCYtU?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DXcWBRiUaG3o5",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/37i9dQZF1DXcWBRiUaG3o5"
                    },
                    "melody": {
                        "youtube": "https://www.youtube.com/embed/NgcBaJhGHbE?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX70RN3TfWWJh",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/37i9dQZF1DX70RN3TfWWJh"
                    },
                    "beats": {
                        "youtube": "https://www.youtube.com/embed/9E6b3swbnWg?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX2pSTOxoPbx9",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/37i9dQZF1DX2pSTOxoPbx9"
                    }
                },

"tamil": {
                    "lofi": {
                        "youtube": "https://www.youtube.com/embed/MGQ5m0QdCjE?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/1E1j2PbaSW1byDCxtaiGlg",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/1E1j2PbaSW1byDCxtaiGlg"
                    },
                    "pop": {
                        "youtube": "https://www.youtube.com/embed/r00ikilDxW4?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DXaVmfUr97Uve",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/37i9dQZF1DXaVmfUr97Uve"
                    },
                    "melody": {
                        "youtube": "https://www.youtube.com/embed/HpEi0lrpLDo?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/4zzmGEbnAkLZRiVO9b9eGO",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/4zzmGEbnAkLZRiVO9b9eGO"
                    },
                    "beats": {
                        "youtube": "https://www.youtube.com/embed/1q8gp2AB6VY?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/43a73ssTnlw00K8ljXDEfO",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/43a73ssTnlw00K8ljXDEfO"
                    }
                }
            },

            # ----------------------------------------------------
            #  MELANCHOLY
            # ----------------------------------------------------
            "melancholy": {
                "english": {
                    "lofi": {
                        "youtube": "https://www.youtube.com/embed/1ZYbU82GVz4?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX7gIoKXt0gmx",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7gIoKXt0gmx"
                    },
                    "pop": {
                        "youtube": "https://www.youtube.com/embed/hLQl3WQQoQ0?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/37i9dQZF1DX7qK8ma5wgG1"
                    },
                    "melody": {
                        "youtube": "https://www.youtube.com/embed/d-diB65scQU?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DWSqBruwoIXkA",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/37i9dQZF1DWSqBruwoIXkA"
                    },
                    "beats": {
                        "youtube": "https://www.youtube.com/embed/oHBx7y8kRPY?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX2pNb5XG6XQH",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/37i9dQZF1DX2pNb5XG6XQH"
                    }
                },

                "tamil": {
                    "lofi": {
                        "youtube": "https://www.youtube.com/embed/MGQ5m0QdCjE?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/1E1j2PbaSW1byDCxtaiGlg",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/1E1j2PbaSW1byDCxtaiGlg"
                    },
                    "pop": {
                        "youtube": "https://www.youtube.com/embed/r00ikilDxW4?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1DXaVmfUr97Uve",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/37i9dQZF1DXaVmfUr97Uve"
                    },
                    "melody": {
                        "youtube": "https://www.youtube.com/embed/HpEi0lrpLDo?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/4zzmGEbnAkLZRiVO9b9eGO",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/4zzmGEbnAkLZRiVO9b9eGO"
                    },
                    "beats": {
                        "youtube": "https://www.youtube.com/embed/1q8gp2AB6VY?autoplay=1",
                        "spotify": "https://open.spotify.com/playlist/43a73ssTnlw00K8ljXDEfO",
                        "spotify_embed": "https://open.spotify.com/embed/playlist/43a73ssTnlw00K8ljXDEfO"
                    }
                }
            }
        }

        # ----------------------------------------------------
        # SAFELY GET PLAYLIST
        # ----------------------------------------------------
        playlist = (
            playlists.get(mood, {})
                     .get(language, {})
                     .get(ptype)
        )

        if not playlist:
            return jsonify({"error": "Invalid mood/language/ptype"}), 400

        # ----------------------------------------------------
        # RETURN FULL YOUTUBE + SPOTIFY PACKAGE
        # ----------------------------------------------------
        return jsonify({
            "playlist_name": f"{language.capitalize()} • {ptype.capitalize()} • {mood.capitalize()}",
            "youtube_url": playlist["youtube"],
            "spotify_url": playlist["spotify"],
            "spotify_embed": playlist["spotify_embed"],
            "description": f"{mood.capitalize()} mood • {language.capitalize()} {ptype} playlist"
        })

    except Exception as e:
        return jsonify({"error": f"Error: {e}"}), 500


# ----------------------------------------------------
# QUOTE API
# ----------------------------------------------------
@app.route('/api/quote', methods=['GET', 'OPTIONS'])
def get_quote():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    quotes = [
        "Success is the sum of small efforts repeated day in and day out. – Robert Collier",
        "Don't watch the clock; do what it does. Keep going. – Sam Levenson",
        "The expert in anything was once a beginner. – Helen Hayes",
        "Education is the most powerful weapon which you can use to change the world. – Nelson Mandela",
        "கல்வி கற்றால் நேர்மை வரும். – திருவள்ளுவர்",
        "அறிவே ஆற்றல். – கலாம்"
    ]
    
    return jsonify({"quote": random.choice(quotes)})

@app.route('/spotify/<path:path>')
def spotify_proxy(path):
    return redirect(f"https://open.spotify.com/{path}")


# ----------------------------------------------------
# ERROR HANDLERS
# ----------------------------------------------------
@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405


# ----------------------------------------------------
# START SERVER
# ----------------------------------------------------
def init_backend():
    print("🚀 Leapcell initializing AI Study Planner backend...")
    print(f"📡 API Key configured: {'YES' if OPENROUTER_API_KEY else 'NO'}")
    print(f"🤖 Model: {OPENROUTER_MODEL}")
    return app
