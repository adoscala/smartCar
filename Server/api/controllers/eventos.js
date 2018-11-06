const mongoose = require('mongoose');
const Evento = require('../models/evento');

exports.eventos_get_all = (req, res, next) => {
    Evento.find().select('-__v').exec().then((docs) => {
        console.log(docs);
        const response = {
            count: docs.length,
            eventos: docs
        };
        res.status(200).json(response)
    }).catch((err) => {
        console.log(err);
        res.status(500).json({ error: err })
    });
}

exports.eventos_create = (req, res, next) => {
    console.log(req);
    const evento = new Evento({
        _id: new mongoose.Types.ObjectId(),
        tipo: req.body.tipo,
        descripcion: req.body.descripcion,
        hora: req.body.hora,
        conductor: req.body.conductor
    });

    evento.save().then((result) => {
        res.status(201).json({
            message: 'El evento fue creado!',
            eventoCreado: evento
        });
    }).catch((err) => {
        console.log(err);
        res.status(500).json({ error: err })
    });
}

exports.eventos_get_evento = (req, res, next) => {
    const idEvento = req.params.id;

    Evento.findById(idEvento).select('-__v').exec().then((doc) => {
        console.log(doc);
        if (doc) {
            res.status(200).json(doc);
        } else {
            res.status(404).json({ message: 'El id no esta asociado a ningun evento'})
        }
    }).catch((err) => {
        console.log(err);
        res.status(500).json({ error: err });
    });
}

exports.eventos_update_evento = (req, res, next) => {
    const idEvento = req.params.id;

    const updateOps = {};
    for (const ops of req.body) {
        updateOps[ops.propName] = ops.value;
    }

    Evento.update({_id: id}, { $set: updateOps }).exec().then((result) => {
        res.status(200).json(result);
    }).catch((err) => {
        console.log(err);
        res.status(500).json({ error: err });
    });

    res.status(200).json({
        message: 'El evento de id = '+ idEvento + ' fue actualizado!'
    });
}

exports.eventos_delete_evento = (req, res, next) => {
    const idEvento = req.params.id;

    Evento.remove({ _id: idEvento }).exec().then((result) => {
        res.status(200).json(result);
    }).catch((err) => {
        console.log(err);
        res.status(500).json({ error: err });
    });
}