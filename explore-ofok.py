# يمكنك استبدال الجزء الخاص بالـ Frontend داخل explore_ofok.py بهذا الكود لإضافة خريطة قمر صناعي تفاعلية:

@app.get("/", response_class=HTMLResponse)
async def get_index():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>Explore Ofok</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
        <!-- مكتبة الخرائط Leaflet CSS -->
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
        <style>
            body { background: #0b132b; color: #edf2f4; font-family: sans-serif; }
            .card { background: #1c2541; color: #fff; border: 1px solid #3a506b; }
            #map { height: 350px; border-radius: 8px; border: 1px solid #3a506b; }
        </style>
    </head>
    <body class="p-4">
        <div class="container">
            <h1 class="text-center text-warning mb-4">Explore Ofok | إكسبلور أفق</h1>
            <div class="row g-4">
                <div class="col-md-6">
                    <div class="card p-4">
                        <h5>اختر الموقع على الخريطة</h5>
                        <!-- عنصر عرض الخريطة -->
                        <div id="map" class="mb-3"></div>
                        <form id="exForm">
                            <input type="text" id="coord" class="form-control mb-2" placeholder="الإحداثيات..." readonly required>
                            <select id="type" class="form-select mb-2">
                                <option value="minerals">استكشاف معادن وذهب</option>
                                <option value="water">استكشاف مياه جوفية</option>
                            </select>
                            <button type="submit" class="btn btn-warning w-100 fw-bold">تحليل الموقع عبر Gemini</button>
                        </form>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card p-4 h-100">
                        <h5>نتيجة التحليل الجيولوجي والثقافي</h5>
                        <div id="result" class="mt-3 text-muted">اضغط على الخريطة لتحديد موقع واضغط "تحليل".</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- مكتبة الخرائط Leaflet JS -->
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            // تهيئة الخريطة على إحداثيات مصر
            const map = L.map('map').setView([29.3084, 30.8428], 9);

            // إضافة طبقة أقمار صناعية عالية الدقة (Esri World Imagery)
            L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                attribution: 'Tiles &copy; Esri'
            }).addTo(map);

            let marker;
            // التقاط الإحداثيات عند النقر على الخريطة
            map.on('click', function(e) {
                const lat = e.latlng.lat.toFixed(5);
                const lng = e.latlng.lng.toFixed(5);
                document.getElementById('coord').value = `${lat}, ${lng}`;
                
                if (marker) map.removeLayer(marker);
                marker = L.marker([lat, lng]).addTo(map);
            });

            // إرسال البيانات للسيرفر
            document.getElementById('exForm').onsubmit = async (e) => {
                e.preventDefault();
                document.getElementById('result').innerHTML = "<div class='spinner-border text-warning'></div> جاري التحليل...";
                
                const f = new FormData();
                f.append('coordinates', document.getElementById('coord').value);
                f.append('target_type', document.getElementById('type').value);
                
                const res = await fetch('/api/explore', {method:'POST', body:f});
                const d = await res.json();
                const j = JSON.parse(d.data);
                
                document.getElementById('result').innerHTML = `
                    <h5 class='text-warning'>${j.location_summary}</h5>
                    <p><strong>المعادن المتوقعة:</strong> ${j.mineral_potential.join(', ')}</p>
                    <p><strong>عمق المياه:</strong> ${j.water_table_depth}</p>
                    <hr>
                    <p class='text-info'><strong>لمحة ثقافية:</strong> ${j.cultural_overview}</p>
                    <a href="https://earth.google.com/web/@${document.getElementById('coord').value.replace(' ', '')},1000a,35d,0y,0h,0t,0r" target="_blank" class="btn btn-outline-info btn-sm">فتح الموقع على Google Earth 🌍</a>
                `;
            };
        </script>
    </body>
    </html>
    """
