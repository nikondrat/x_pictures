import 'package:flutter/widgets.dart';
import 'package:x_pictures/src/data.dart';

class AppBody extends StatelessWidget {
  final Widget Function(
      double windowWidth, double windowHeight, WindowSize windowSize) builder;
  const AppBody({super.key, required this.builder});

  @override
  Widget build(BuildContext context) {
    final windowWidth = MediaQuery.sizeOf(context).width;
    final windowHeight = MediaQuery.sizeOf(context).height;

    return LayoutBuilder(builder: (context, constraints) {
      final windowSize = constraints.materialBreakpoint;

      return builder(windowWidth, windowHeight, windowSize);
    });
  }
}
