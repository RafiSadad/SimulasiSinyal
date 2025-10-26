use serde::{Deserialize, Serialize};
use std::f64::consts::PI;

// Struktur untuk menampung parameter sinyal dari frontend [cite: 268, 300-302]
#[derive(Serialize, Deserialize, Clone)]
pub struct SignalParams {
    pub amplitude: f64, // A
    pub frequency: f64, // f
    pub phase: f64,     // φ (dalam radian)
}

// Fungsi untuk menghasilkan satu sinyal sinusoidal [cite: 268]
pub fn generate_signal(params: &SignalParams, t: &Vec<f64>) -> Vec<f64> {
    t.iter()
     .map(|&ti| params.amplitude * (2.0 * PI * params.frequency * ti + params.phase).sin())
     .collect()
}

// Fungsi untuk menjumlahkan dua sinyal [cite: 107, 270]
pub fn add_signals(x1: &Vec<f64>, x2: &Vec<f64>) -> Vec<f64> {
    x1.iter().zip(x2).map(|(a, b)| a + b).collect()
}

// Fungsi untuk mengurangi dua sinyal [cite: 215, 272]
pub fn subtract_signals(x1: &Vec<f64>, x2: &Vec<f64>) -> Vec<f64> {
    x1.iter().zip(x2).map(|(a, b)| a - b).collect()
}

// Fungsi untuk mengalikan dua sinyal [cite: 427, 274]
pub fn multiply_signals(x1: &Vec<f64>, x2: &Vec<f64>) -> Vec<f64> {
    x1.iter().zip(x2).map(|(a, b)| a * b).collect()
}