

//Da formato al problema escrito, aunque en un principio no hay nada, *se podria borrar
var problemSpan = document.getElementById('problem');
MQ.StaticMath(problemSpan);

//campo para escribir el problema, define el campo mathquill editable
var answerSpan = document.getElementById('answer');
var answerMathField = MQ.MathField(answerSpan, {
    handlers: {
    edit: function() {
        var enteredMath = answerMathField.latex(); // Get entered math in LaTeX format

        //escribe por consola el texto escrito en formato LaTeX, es para probar, *se puede borrar
        //console.log(enteredMath);
        
        //boton escribe el problema editado en pantalla
        function escribe(){
            document.getElementById("problem").innerHTML =enteredMath;
            //jQuery para añdir la pregunta en latex a un input
            $("#pregunta_math").val(enteredMath);
        }
        document.getElementById("boton-escribir").onclick = function(){
            escribe();
            //cambia el formato de latex para visualizarlo en mathquill
            var problemSpan = document.getElementById('problem');
            MQ.StaticMath(problemSpan);

        }
        
    }
    }
  
});


//BOTONES

// raiz cuadrada
var raizCuadrada = document.getElementById('raizCuadrada');
MQ.StaticMath(raizCuadrada);

function botonRaizCuadrada(){
    answerMathField.cmd('\\sqrt'); 
    answerMathField.focus() // centra el cursor en la ultima función escrita
}
document.getElementById("raizCuadrada").onclick = function(){
    botonRaizCuadrada();
}

// elevar al cuadrado
var xAlCuadrado = document.getElementById('xAlCuadrado');
MQ.StaticMath(xAlCuadrado);

function botonxAlCuadrado(){
    answerMathField.write('^{2}'); 
    answerMathField.focus() // centra el cursor en la ultima función escrita
}
document.getElementById("xAlCuadrado").onclick = function(){
    botonxAlCuadrado();
}

//elevar

var elevar = document.getElementById('elevar');
MQ.StaticMath(elevar);

function botonelevar(){
    answerMathField.cmd('^'); 
    answerMathField.focus() // centra el cursor en la ultima función escrita
}
document.getElementById("elevar").onclick = function(){
    botonelevar();
}

//raiz n
var raizN = document.getElementById('raizN');
MQ.StaticMath(raizN);

function botonraizN(){
    answerMathField.cmd('\\nthroot'); 
    answerMathField.focus() // centra el cursor en la ultima función escrita
}
document.getElementById("raizN").onclick = function(){
    botonraizN();
}


//fraccion
var fraccion = document.getElementById('fraccion');
MQ.StaticMath(fraccion);

function botonfraccion(){
    answerMathField.write('\\frac{}{}'); 
    answerMathField.focus() // centra el cursor en la ultima función escrita
}
document.getElementById("fraccion").onclick = function(){
    botonfraccion();
}


//logaritmo
var logaritmo = document.getElementById('logaritmo');
MQ.StaticMath(logaritmo);

function botonlogaritmo(){
    answerMathField.write('\\log_{}()'); 
    answerMathField.focus() // centra el cursor en la ultima función escrita
}
document.getElementById("logaritmo").onclick = function(){
    botonlogaritmo();
}

//limite
var limite = document.getElementById('limite');
MQ.StaticMath(limite);

function botonlimite(){
    answerMathField.write('\lim_{ {x} \\to \\infty }( )'); 
    answerMathField.focus() // centra el cursor en la ultima función escrita
}
document.getElementById("limite").onclick = function(){
    botonlimite();
}