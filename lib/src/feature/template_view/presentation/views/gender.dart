import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';
import 'package:gap/gap.dart';

class GenderView extends StatelessWidget {
  const GenderView({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          leading: const CustomBackButton(),
          title: Text(t.auth.title),
        ),
        body: AppBody(
          builder: (windowWidth, windowHeight, windowSize) {
            return ListView(
              padding: HorizontalSpacing.centered(windowWidth),
              children: [
                Center(child: Text('hi'),)
              ],
            );
          },
        ));
  }
}
