import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class SliverGridView extends StatelessWidget {
  const SliverGridView({super.key});

  @override
  Widget build(BuildContext context) {
    return SliverGrid(
      delegate: SliverChildBuilderDelegate(
        (context, index) {
          return const ImageItemOfficePage();
        },
        childCount: 20,
      ),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        childAspectRatio: .8,
        mainAxisSpacing: 15,
        crossAxisSpacing: 15,
      ),
    );
  }
}
