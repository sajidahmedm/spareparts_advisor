from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# -----------------------
# 2-WHEELER PARTS
# -----------------------
two_wheeler_parts = {
    "Crankshaft": {
        "description": "Converts the linear motion of the pistons into rotational motion.",
        "usage": "Located inside the engine; essential for converting piston movement to drive power."
    },
    "Cylinder Head": {
        "description": "Houses the valves and other components related to the combustion process.",
        "usage": "Mounted on top of the cylinder block; key for combustion control."
    },
    "Piston & Rings": {
        "description": "Convert fuel into mechanical energy as part of the combustion process.",
        "usage": "Operate within the cylinder; allow compression and transfer energy to the crankshaft."
    },
    "Connecting Rod": {
        "description": "Connects the piston to the crankshaft.",
        "usage": "Transmits motion and force from the piston to the crankshaft."
    },
    "Valves": {
        "description": "Control the flow of air and fuel into the cylinder and exhaust gases out.",
        "usage": "Mounted in the cylinder head; opens/closes for air-fuel and exhaust management."
    },
    "Battery": {
        "description": "Stores electrical energy to start the engine and power other components.",
        "usage": "Provides initial energy for engine startup and supports electrical load."
    },
    "Alternator": {
        "description": "Generates electricity to charge the battery and power the system.",
        "usage": "Mounted on the engine; driven by belt or gear."
    },
    "Starter Motor": {
        "description": "Provides the initial rotational force to start the engine.",
        "usage": "Engages with the engine's flywheel to initiate engine rotation."
    },
    "Wiring Harness": {
        "description": "Connects all the electrical components together.",
        "usage": "Runs through the vehicle connecting power and signals."
    },
    "Ignition System": {
        "description": "Ignites the fuel-air mixture via spark plug and coil.",
        "usage": "Starts combustion in the engine cylinders."
    },
    "Fairings": {
        "description": "Plastic/fiberglass panels covering and protecting the engine.",
        "usage": "Provide aerodynamic shape and protect internal parts."
    },
    "Fenders": {
        "description": "Protect the rider from debris and water spray.",
        "usage": "Mounted over the wheels; guard against splashes."
    },
    "Mirrors": {
        "description": "Provide the rider with rear and side visibility.",
        "usage": "Mounted on handlebars or fairings."
    },
    "Chassis/Frame": {
        "description": "The structural backbone of the vehicle.",
        "usage": "Supports all mechanical parts including engine and suspension."
    },
    "Seat": {
        "description": "Provides a comfortable area for the rider.",
        "usage": "Mounted on frame, usually above the rear wheel."
    },
    "Lights": {
        "description": "Headlight, taillight, brake light, and turn signals.",
        "usage": "Essential for visibility and safety."
    },
    "Clutch": {
        "description": "Disengages and engages the engine power to the transmission.",
        "usage": "Operated via lever to change gears smoothly."
    },
    "Gears": {
        "description": "Change the gear ratio to optimize power and speed.",
        "usage": "Mounted inside gearbox; engaged sequentially."
    },
    "Chain/Belt": {
        "description": "Transmits power from the engine to the rear wheel.",
        "usage": "Looped around sprockets or pulleys."
    },
    "Shocks/Struts": {
        "description": "Absorb road shocks and vibrations.",
        "usage": "Mounted near wheels for ride comfort."
    },
    "Springs": {
        "description": "Support vehicle weight and help dampen impacts.",
        "usage": "Work with shocks in suspension system."
    },
    "Swingarm": {
        "description": "Connects the rear wheel to the frame.",
        "usage": "Holds the rear wheel and pivots for suspension travel."
    },
    "Brake Pads": {
        "description": "Friction material that slows the vehicle down.",
        "usage": "Pressed against brake rotors in disc brakes."
    },
    "Brake Calipers": {
        "description": "Hold brake pads and apply pressure.",
        "usage": "Hydraulically actuated; clamps brake rotors."
    },
    "Brake Rotors": {
        "description": "The disc that brake pads clamp onto.",
        "usage": "Mounted on wheels; dissipates kinetic energy as heat."
    },
    "Brake Levers/Pedals": {
        "description": "Control the braking system.",
        "usage": "Actuate master cylinder to apply brakes."
    },
    "Wheels": {
        "description": "Support tires and allow motion.",
        "usage": "Connect tires to axles; enable rotation."
    },
    "Tires": {
        "description": "Provide road contact and grip.",
        "usage": "Mounted on wheels; ensure traction and handling."
    }
}

# -----------------------
# 4-WHEELER PARTS
# -----------------------
four_wheeler_parts = {
    "Radiator": {
        "description": "Cools the engine by dissipating heat from coolant.",
        "usage": "Mounted at the front; connected to engine cooling system."
    },
    "Fuel Injector": {
        "description": "Sprays fuel into the engine for combustion.",
        "usage": "Mounted on intake manifold or engine head."
    },
    "Catalytic Converter": {
        "description": "Reduces harmful exhaust emissions.",
        "usage": "Part of exhaust system under the car."
    },
    "AC Compressor": {
        "description": "Compresses refrigerant to enable cabin cooling.",
        "usage": "Driven by engine belt; part of AC system."
    },
    "Power Steering Pump": {
        "description": "Assists steering by hydraulic or electric means.",
        "usage": "Mounted near engine; helps ease turning of the wheel."
    },
    "ECU": {
        "description": "Controls engine operations electronically.",
        "usage": "Central computer that manages engine performance."
    },
    "Timing Belt": {
        "description": "Coordinates crankshaft and camshaft timing.",
        "usage": "Runs internal combustion engine with proper valve timing."
    },
    "Disc Brake": {
        "description": "Braking system using disc and calipers.",
        "usage": "Slows down wheels by friction at rotors."
    },
    "Shock Absorber": {
        "description": "Dampens suspension movement for smoother ride.",
        "usage": "Connected to suspension to absorb shocks."
    },
    "Transmission": {
        "description": "Changes gear ratios to transfer engine power.",
        "usage": "Connects engine to driveshaft and wheels."
    },
    "Differential": {
        "description": "Allows wheels to rotate at different speeds.",
        "usage": "Key in turning and cornering stability."
    },
    "Oil Filter": {
        "description": "Filters contaminants from engine oil.",
        "usage": "Mounted near engine oil line."
    },
    "Air Filter": {
        "description": "Prevents dust from entering the engine.",
        "usage": "Located before the intake manifold."
    },
    "Headlight": {
        "description": "Provides illumination at night and visibility.",
        "usage": "Mounted at the front of the vehicle."
    },
    "Tail Light": {
        "description": "Signals braking and night-time visibility.",
        "usage": "Mounted at the rear of the car."
    },
    "Horn": {
        "description": "Produces audible warning sound.",
        "usage": "Activated by steering wheel button."
    },
    "Wiper Motor": {
        "description": "Drives the windshield wipers.",
        "usage": "Ensures visibility during rain/snow."
    },
    "Window Regulator": {
        "description": "Raises and lowers car windows.",
        "usage": "Mounted inside door panel."
    },
    "Clutch Plate": {
        "description": "Engages/disengages power from engine to gearbox.",
        "usage": "Between flywheel and transmission input shaft."
    },
    "Flywheel": {
        "description": "Stores rotational energy from engine.",
        "usage": "Attached to crankshaft; maintains engine momentum."
    }
}

# -----------------------
# API ROUTE
# -----------------------
@app.route("/")
def home():
    return "Backend is running 🚀"
@app.route("/get_info", methods=["POST"])
def get_info():
    data = request.get_json()
    part = data.get("part")
    vehicle_type = data.get("vehicle_type", "2-wheeler").lower()

    db = two_wheeler_parts if vehicle_type == "2-wheeler" else four_wheeler_parts

    if part in db:
        info = db[part]
        query = part.replace(" ", "+")
        videos = {
            "English": f"https://www.youtube.com/results?search_query={query}+{vehicle_type}+part+explained+in+english",
            "Hindi": f"https://www.youtube.com/results?search_query={query}+{vehicle_type}+part+explained+in+hindi",
            "Telugu": f"https://www.youtube.com/results?search_query={query}+{vehicle_type}+part+explained+in+telugu"
        }

        return jsonify({
            "name": part,
            "description": info["description"],
            "usage": info["usage"],
            "videos": videos
        })
    else:
        return jsonify({"error": f"{vehicle_type.capitalize()} part not found"}), 404


if __name__ == "__main__":
    app.run()
