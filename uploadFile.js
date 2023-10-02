const express = require('express')
const multer = require('multer')
const multerS3 = require('multer-s3')
const { S3Client } = require('@aws-sdk/client-s3')

const app = express()
const port = 3001
const s3 = new S3Client()

const upload = multer({
    storage: multerS3({
        s3: s3,
        bucket: 'storiapp',
        metadata: function (req, file, cb) {
            cb(null, { fieldName: file.fieldname });
        },
        key: function (req, file, cb) {
            cb(null, Date.now().toString() + '.csv')
        }
    })
})

app.post('/api/upload-csv', upload.single('file'), (req, res) => {
    return res.json({
        msg: 'File successfully uploaded!',
        file: req.file,
    })
})
app.listen(port, () => {
    console.log(`listening on port http://localhost:${port}/api/upload-csv`)
})