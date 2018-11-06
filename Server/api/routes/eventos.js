const express = require('express');
const router = express.Router();
const multer = require('multer');
// const checkAuth = require('../middleware/check-auth');
const EventosController = require('../controllers/eventos')

router.get('/', EventosController.eventos_get_all );

router.post('/crear', EventosController.eventos_create);

router.get('/:id', EventosController.eventos_get_evento);

router.patch('/:id', EventosController.eventos_update_evento);

router.delete('/:id', EventosController.eventos_delete_evento);

module.exports = router;