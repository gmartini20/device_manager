/*
 * cryptoHelpers.js: implements AES - Advanced Encryption Standard
 * from the SlowAES project, http://code.google.com/p/slowaes/
 * 
 * Copyright (c) 2008     Josh Davis ( http://www.josh-davis.org ),
 *                        Mark Percival ( http://mpercival.com ),
 *                        Johan Sundstrom ( http://ecmanaut.blogspot.com ),
 *                         John Resig ( http://ejohn.org )
 * 
 * Licensed under the Apache License, Version 2.0
 * http://www.apache.org/licenses/
 */

var cryptoHelpers = {
    // encodes a unicode string to UTF8 (8 bit characters are critical to AES functioning properly)

    convertStringToByteArray: function(s)
    {
        var byteArray = [];
        for(var i = 0;i < s.length;i++)
                {
                        byteArray.push(s.charCodeAt(i));
                }
        return byteArray;
    },

    convertByteArrayToString: function(byteArray)
    {
        var s = '';
        for(var i = 0;i < byteArray.length;i++)
                {
                        s += String.fromCharCode(byteArray[i])
                }
        return s;
    },
    
    base64: {
        // Takes a Nx16x1 byte array and converts it to Base64
        chars: [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
        'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
        'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
        'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
        'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
        'w', 'x', 'y', 'z', '0', '1', '2', '3',
        '4', '5', '6', '7', '8', '9', '+', '/',
        '=', // for decoding purposes
        ],
    
        encode_line: function(flatArr){
            var b64 = '';

            for (var i = 0; i < flatArr.length; i += 3){
                b64 += this.chars[flatArr[i] >> 2];
                b64 += this.chars[((flatArr[i] & 3) << 4) | (flatArr[i + 1] >> 4)];
                if (!(flatArr[i + 1] == null)){
                    b64 += this.chars[((flatArr[i + 1] & 15) << 2) | (flatArr[i + 2] >> 6)];
                }else{
                    b64 += '=';
                }
                if (!(flatArr[i + 2] == null)){
                    b64 += this.chars[flatArr[i + 2] & 63];
                }else{
                    b64 += '=';
                }
            }
            return b64;
        },
    
        encode: function(flatArr)
        {
            var b64 = this.encode_line(flatArr);
            // OpenSSL is super particular about line breaks
            var broken_b64 = b64.slice(0, 64) + '\n';
            for (var i = 1; i < (Math.ceil(b64.length / 64)); i++)
            {
                broken_b64 += b64.slice(i * 64, i * 64 + 64) + (Math.ceil(b64.length / 64) == i + 1 ? '': '\n');
            }
            return broken_b64;
        },
    
        decode64: function (input)
        {
            var keyStr = "ABCDEFGHIJKLMNOP" +
               "QRSTUVWXYZabcdef" +
               "ghijklmnopqrstuv" +
               "wxyz0123456789+/" +
               "=";
            var output = "";
            var chr1, chr2, chr3 = "";
            var enc1, enc2, enc3, enc4 = "";
            var i = 0;
	 
            // remove all characters that are not A-Z, a-z, 0-9, +, /, or =
            var base64test = /[^A-Za-z0-9\+\/\=/\"]/g;
            if (base64test.exec(input)) {
                alert("There were invalid base64 characters in the input text.\n" +
                      "Valid base64 characters are A-Z, a-z, 0-9, '+', '/',and '='\n" +
                      "Expect errors in decoding.");
            }
            input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");

            do {
                enc1 = keyStr.indexOf(input.charAt(i++));
                enc2 = keyStr.indexOf(input.charAt(i++));
                enc3 = keyStr.indexOf(input.charAt(i++));
                enc4 = keyStr.indexOf(input.charAt(i++));

                chr1 = (enc1 << 2) | (enc2 >> 4);
                chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
                chr3 = ((enc3 & 3) << 6) | enc4;

                output = output + String.fromCharCode(chr1);

                if (enc3 != 64) {
                    output = output + String.fromCharCode(chr2);
                }
                if (enc4 != 64) {
                    output = output + String.fromCharCode(chr3);
                }

                chr1 = chr2 = chr3 = "";
                enc1 = enc2 = enc3 = enc4 = "";

            } while (i < input.length);

            return unescape(output);
        },

        
    },
    
};
