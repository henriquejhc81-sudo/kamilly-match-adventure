import 'dart:math';
import 'package:flutter/material.dart';
import 'package:audioplayers/audioplayers.dart';

void main() => runApp(MaterialApp(home: RoletaVivaSorte()));

class RoletaVivaSorte extends StatefulWidget {
  @override
  _RoletaVivaSorteState createState() => _RoletaVivaSorteState();
}

class _RoletaVivaSorteState extends State<RoletaVivaSorte> with SingleTickerProviderStateMixin {
  // Controle de Saldo e Som
  double saldo = 100.0;
  double custoJogada = 5.0;
  final AudioPlayer _audioPlayer = AudioPlayer();
  
  // Controle da Animação
  late AnimationController _controller;
  late Animation<double> _animation;
  double _anguloFinal = 0.0;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: Duration(seconds: 4));
    _animation = CurvedAnimation(parent: _controller, curve: Curves.decelerate);
  }

  void _girarRoleta() async {
    // 1. VERIFICAÇÃO E SUBTRAÇÃO DE SALDO
    if (saldo < custoJogada) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Saldo Insuficiente!")));
      return;
    }

    setState(() {
      saldo -= custoJogada; // Subtrai o valor antes de girar
    });

    // 2. TOCA O SOM (CORREÇÃO DO SOM)
    await _audioPlayer.play(AssetSource('audios/spin_sound.mp3'));

    // 3. LÓGICA DE SORTEIO
    Random random = Random();
    double giroAdicional = random.nextDouble() * 2 * pi; // Define onde vai parar
    _anguloFinal += (2 * pi * 5) + giroAdicional; // 5 voltas completas + sorteio

    _controller.forward(from: 0.0).then((_) {
      _processarPremio(giroAdicional); // RECONHECE A PREMIAÇÃO
    });
  }

  void _processarPremio(double angulo) {
    // Exemplo simples: divide a roleta em 4 partes
    setState(() {
      if (angulo < pi / 2) {
        saldo += 10.0; // Ganhou 10
        print("Ganhou R\$ 10!");
      } else if (angulo < pi) {
        print("Tente novamente!");
      } else {
        saldo += 2.0; // Ganhou 2
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.green,
      appBar: AppBar(title: Text("Viva a Sorte - Roleta")),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text("SALDO: R\$ ${saldo.toStringAsFixed(2)}", 
               style: TextStyle(color: Colors.white, fontSize: 32, fontWeight: FontWeight.bold)),
          SizedBox(height: 50),
          AnimatedBuilder(
            animation: _animation,
            builder: (context, child) {
              return Transform.rotate(
                angle: _animation.value * _anguloFinal,
                child: Image.asset('assets/images/roleta.png', width: 300),
              );
            },
          ),
          SizedBox(height: 50),
          ElevatedButton(
            onPressed: _controller.isAnimating ? null : _girarRoleta,
            child: Text("GIRAR (R\$ 5.00)", style: TextStyle(fontSize: 20)),
            style: ElevatedButton.styleFrom(padding: EdgeInsets.symmetric(horizontal: 50, vertical: 20)),
          )
        ],
      ),
    );
  }
}
