from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ذخیره وضعیت پین‌ها در حافظه سرور (پیش‌فرض همه خاموش)
gpio_states = {str(i): "0" for i in range(9)}
# نام پیش‌فرض پین‌ها
pin_names = ["GPIO16", "GPIO5", "GPIO4", "GPIO0*", "GPIO2*", "GPIO14", "GPIO12", "GPIO13", "GPIO15*"]

# صفحه وب اصلی برای کنترل دکمه‌ها از راه دور
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ESP Cloud Control</title>
    <style>
        body { background: #050a14; color: #c8deff; font-family: sans-serif; text-align: center; padding: 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; max-width: 600px; margin: 20px auto; }
        .card { background: #0f1f3a; padding: 15px; border-radius: 10px; border: 1px solid rgba(0,229,255,0.2); }
        .btn { background: #ff3060; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; }
        .btn.on { background: #00ff88; color: #050a14; }
    </style>
</head>
<body>
    <h1>ESP Cloud Control Panel</h1>
    <div class="grid">
        {% for i in range(9) %}
        <div class="card">
            <h3>{{ pin_names[i] }}</h3>
            <button class="btn {% if states[str(i)] == '1' %}on{% endif %}" onclick="toggle('{{ i }}')">
                {% if states[str(i)] == '1' %}ON{% else %}OFF{% endif %}
            </button>
        </div>
        {% endfor %}
    </div>
    <script>
        function toggle(id) {
            fetch('/toggle?pin=' + id).then(() => location.reload());
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, states=gpio_states, pin_names=pin_names)

# تغییر وضعیت پین از طریق وب‌سایت
@app.route('/toggle')
def toggle():
    pin = request.args.get('pin')
    if pin in gpio_states:
        gpio_states[pin] = "1" if gpio_states[pin] == "0" else "0"
    return "OK"

# این دیتایی است که ESP8266 هر چند ثانیه یک‌بار دانلود می‌کند
@app.route('/api/status')
def get_status():
    return jsonify(gpio_states)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)