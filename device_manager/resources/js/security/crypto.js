define(function (require) {

    return {
        criptografarCredenciais: function (cryptoParams) {
            var chaveString = cryptoHelpers.base64.decode64(cryptoParams.salt);
            var chave = cryptoHelpers.convertStringToByteArray(chaveString);
            var IVString = cryptoHelpers.base64.decode64("AAAAAAAAAAAAAAAAAAAAAA==");
            var IV = cryptoHelpers.convertStringToByteArray(IVString);
            var senhaBytesToEncrypt = cryptoHelpers.convertStringToByteArray(cryptoParams.senha);
            var usuarioBytesToEncrypt = cryptoHelpers.convertStringToByteArray(cryptoParams.usuario);
            var senhaResult = slowAES.encrypt(senhaBytesToEncrypt, slowAES.modeOfOperation.CBC, chave, slowAES.aes.keySize.SIZE_256, IV);
            var usuarioResult = slowAES.encrypt(usuarioBytesToEncrypt, slowAES.modeOfOperation.CBC, chave, slowAES.aes.keySize.SIZE_256, IV);
            var data = { "Nome": cryptoHelpers.base64.encode(usuarioResult), "Senha": cryptoHelpers.base64.encode(senhaResult) };
            return data;
        },

        criptografar: function (plainText, salt) {
            var chaveString = cryptoHelpers.base64.decode64(salt);
            var chave = cryptoHelpers.convertStringToByteArray(chaveString);
            var IVString = cryptoHelpers.base64.decode64("AAAAAAAAAAAAAAAAAAAAAA==");
            var IV = cryptoHelpers.convertStringToByteArray(IVString);
            var senhaBytesToEncrypt = cryptoHelpers.convertStringToByteArray(plainText);
            var senhaResult = slowAES.encrypt(senhaBytesToEncrypt, slowAES.modeOfOperation.CBC, chave, slowAES.aes.keySize.SIZE_256, IV);            
            return cryptoHelpers.base64.encode(senhaResult);
        }
    }
});