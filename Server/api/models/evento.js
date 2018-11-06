const mongoose = require("mongoose");

const eventosSchema = mongoose.Schema({
    _id: mongoose.Schema.Types.ObjectId,
    tipo: {type: String, required: true},
    descripcion: {type: String, required: true},
    hora: {type: String, required: false},
    conductor: {type: JSON, required: true}
});

module.exports = mongoose.model('Evento', eventosSchema);