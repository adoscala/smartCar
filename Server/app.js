const express = require('express');
const app = express();
const morgan = require('morgan');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
var cors = require('cors')


const eventosRoutes = require('./api/routes/eventos');

 // mongoose.connect('mongodb+srv://smartcar:paula1234%24@smartcar-60ejd.mongodb.net/test?retryWrites=false');
 mongoose.connect('mongodb://prios:paulita@smartcar-shard-00-00-60ejd.mongodb.net:27017,smartcar-shard-00-01-60ejd.mongodb.net:27017,smartcar-shard-00-02-60ejd.mongodb.net:27017/test?ssl=true&replicaSet=smartcar-shard-0&authSource=admin&retryWrites=false');

app.use(morgan('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use(cors());

// // CORS Allow
// app.use((req, res, next) => {
//     res.header('Allow-Control-Allow-Origin', '*');
//     res.header('Allow-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
//     res.header('Access-Control-Allow-Origin','*');
//
//     if(req.method === 'OPTIONS') {
//         res.header('Allow-Control-Allow-Methods', 'PUT, POST, GET, PATCH, DELETE');
//         return res.status(200).json({});
//     }
//     next();
// });

// Rutas
app.use('/eventos', eventosRoutes);

// Si la peticion pasa por todas las rutas
app.use((req, res, next) => {
    const error = new Error('Not Found');
    error.status = 404;
    next(error);    // Envia la peticion all middleware siguiente
});

app.use((error, req, res, next) => {
    res.status(error.status || 500);
    res.json({
        error: error.message
    });
});

module.exports = app;
