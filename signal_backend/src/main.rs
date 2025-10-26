use actix_web::{web, App, HttpServer, Responder, HttpResponse};
use serde::{Deserialize, Serialize};

// Impor modul logika sinyal kita
mod processor;
use processor::{SignalParams, generate_signal, add_signals, subtract_signals, multiply_signals};

// Struktur data untuk request dari frontend [cite: 300-303]
#[derive(Deserialize)]
struct SimulationRequest {
    params1: SignalParams,      // Parameter untuk x1(t)
    params2: SignalParams,      // Parameter untuk x2(t)
    operation: String,          // "add", "subtract", atau "multiply"
    fs: f64,                    // Frekuensi sampling
    duration_secs: f64,         // Durasi simulasi
}

// Struktur data untuk respons JSON ke frontend [cite: 284]
#[derive(Serialize)]
struct SimulationResponse {
    t: Vec<f64>,  // Vektor waktu
    x1: Vec<f64>, // Sinyal x1
    x2: Vec<f64>, // Sinyal x2
    y: Vec<f64>,  // Sinyal hasil y
}

// Handler untuk endpoint /simulate
async fn simulate(req: web::Json<SimulationRequest>) -> impl Responder {
    let num_samples = (req.fs * req.duration_secs) as usize;
    let t: Vec<f64> = (0..num_samples).map(|n| n as f64 / req.fs).collect();

    let x1 = generate_signal(&req.params1, &t);
    let x2 = generate_signal(&req.params2, &t);

    // Memilih operasi berdasarkan request [cite: 270, 272, 274]
    let y = match req.operation.as_str() {
        "add" => add_signals(&x1, &x2),
        "subtract" => subtract_signals(&x1, &x2),
        "multiply" => multiply_signals(&x1, &x2),
        _ => vec![0.0; num_samples], // Default case jika operasi tidak valid
    };

    HttpResponse::Ok().json(SimulationResponse { t, x1, x2, y })
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    println!("Backend server berjalan di http://127.0.0.1:8080");
    
    HttpServer::new(|| {
        App::new()
            .route("/simulate", web::post().to(simulate))
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}