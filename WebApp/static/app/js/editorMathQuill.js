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
        //antigua funcion 
        //function escribe(id_of_input){
            //document.getElementById("answer").innerHTML =enteredMath;
            //jQuery para añdir la pregunta en latex a un input
            //$("#id_texto").val('\\(' + enteredMath +'\\)');
            //var input_id = '#'+id_of_input;
            //$(input_id).val($(input_id).val() + enteredMath);}
        
        
        //boton escribe el problema editado en pantalla
        function escribe(id_of_input){
            document.getElementById("problem").innerHTML =enteredMath;
    
            var input_id = '#'+id_of_input;
            $(input_id).val($(input_id).val() + (' \\(' + enteredMath +'\\)') );
        }
        document.getElementById("boton-escribir").onclick = function(){
            escribe("id_texto");
            //cambia el formato de latex para visualizarlo en mathquill
            var problemSpan = document.getElementById('problem');
            MQ.StaticMath(problemSpan);

        }
        
    }
    }
  
});

/* //posible función para previsualizar la pregunta escrita
function previsualizar(){
    preguntaCreada = $("#id_texto").val();
    console.log(preguntaCreada);
    document.getElementById("previzualizacion-pregunta").innerHTML= preguntaCreada;
}
document.getElementById("ver-pregunta").onclick = function(){
    previsualizar();
}

*/


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
    answerMathField.write('\\lim_{ {x} \\to \\infty }( )'); 
    answerMathField.focus() // centra el cursor en la ultima función escrita
}
document.getElementById("limite").onclick = function(){
    botonlimite();
}

//pi
var pi = document.getElementById('pi');
MQ.StaticMath(pi);

function botonpi(){
    answerMathField.write('\\pi'); 
    answerMathField.focus() // centra el cursor en la ultima función escrita
}
document.getElementById("pi").onclick = function(){
    botonpi();
}

//theta
var theta = document.getElementById('theta');
MQ.StaticMath(theta);

function botontheta(){
    answerMathField.write('\\theta'); 
    answerMathField.focus() // centra el cursor en la ultima función escrita
}
document.getElementById("theta").onclick = function(){
    botontheta();
}

//infinito
var inf = document.getElementById('inf');
MQ.StaticMath(inf);

function botoninf(){
    answerMathField.write('\\infty'); 
    answerMathField.focus() // centra el cursor en la ultima función escrita
}
document.getElementById("inf").onclick = function(){
    botoninf();
}

//integral
var integral = document.getElementById('integral');
MQ.StaticMath(integral);

function botonintegral(){
    answerMathField.write('\\int_{}'); 
    answerMathField.focus() // centra el cursor en la ultima función escrita
}
document.getElementById("integral").onclick = function(){
    botonintegral();
}

//derivada
var derivada = document.getElementById('derivada');
MQ.StaticMath(derivada);

function botonderivada(){
    answerMathField.write('\\frac{d}{dx}\\left(\\right)'); 
    answerMathField.focus() // centra el cursor en la ultima función escrita
}
document.getElementById("derivada").onclick = function(){
    botonderivada();
}