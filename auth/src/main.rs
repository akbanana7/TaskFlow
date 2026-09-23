use axum::{ // Imports axum library
    routing::get,
    Router
};

#[tokio::main()]

async fn main() {
    // `Router::new()` has a generic state type. Without an explicit type,
    // Rust cannot infer that state from this route, so specify the default
    // unit state (`()`) explicitly.
    let app: Router<()> = Router::new()
        .route("/", get(up));

    // This does something fancy to listen on a port
    let listener = tokio::net::TcpListener::bind("0.0.0.0:8090").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn up() -> &'static str{ // Essentially spits back "yup" in a http GET request when accessing initial url/ip
    "yup"
}
