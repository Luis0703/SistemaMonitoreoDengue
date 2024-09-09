const express = require('express');  // Asegúrate de tener express importado correctamente
const passport = require('passport');  // Asegúrate de tener passport
const GoogleStrategy = require('passport-google-oauth20').Strategy;  // Esta es la estrategia de Google OAuth
const cookieSession = require('cookie-session');  // Importa cookie-session para manejar las sesiones

const app = express();

// Configurar cookie-session
app.use(cookieSession({
  name: 'session',
  keys: ['key1', 'key2']
}));

// Inicializar passport
app.use(passport.initialize());
app.use(passport.session());

// Configurar serialización y deserialización de usuarios
passport.serializeUser((user, done) => {
  done(null, user);
});

passport.deserializeUser((user, done) => {
  done(null, user);
});

// Configurar estrategia de Google OAuth
passport.use(new GoogleStrategy({
    clientID: '1097152974481-13oehkt0sd8u9hkt49akfp5p6j25cmeg.apps.googleusercontent.com',
    clientSecret: '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',
  callbackURL: '/auth/google/callback'
},
function(accessToken, refreshToken, profile, done) {
  // Aquí puedes manejar el perfil del usuario y cualquier lógica de autenticación
  return done(null, profile);
}));

// Ruta para redirigir a Google
app.get('/auth/google', passport.authenticate('google', {
  scope: ['profile', 'email']
}));

// Ruta de callback de Google
app.get('/auth/google/callback',
  passport.authenticate('google', { failureRedirect: '/' }),
  (req, res) => {
    // Redirige al usuario a la página que desees después de la autenticación
    res.redirect('/');
  }
);

// Ruta de logout
app.get('/logout', (req, res) => {
  req.logout();
  res.redirect('/');
});

// Inicializar servidor
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
