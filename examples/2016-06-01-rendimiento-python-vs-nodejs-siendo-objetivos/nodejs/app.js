const express = require('express');

// Constants
const PORT = 8080;

// App
const app = express();

// End-points
app.get('/', (req, res) => {
  res.send(`<!DOCTYPE html>
<html lang="es">
<head>
	<title>Hello world!</title>
</head>
<body>
<p>Página de prueba</p>
</body>
</html>`);
});

app.get('/json', (req, res) => {
  res.json({ test: 1, data: "hello world" });
});

// Start server
app.listen(PORT, null, 5000, () => {
  console.log(`Running on http://localhost:${PORT}`);
});
