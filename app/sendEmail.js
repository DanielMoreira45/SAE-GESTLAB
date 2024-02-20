const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'gestlab.team@gmail.com',
    pass: 'Gestlab45!!',
  },
});

const mailOptions = {
  from: 'gestlab.team@gmail.com',
  // to: 'cassandra.maupou.etu@gmail.com',
  to: 'amelie.brizardpro@laposte.net',
  subject: 'Subject of the email',
  text: 'This is the body of the email.',
};

transporter.sendMail(mailOptions, (error, info) => {
  if (error) {
    console.error(error);
  } else {
    console.log('Email sent: ' + info.response);
  }
});
