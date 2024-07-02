import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class GenerateStyles extends StatelessWidget {
  const GenerateStyles({super.key});

  @override
  Widget build(BuildContext context) {
    return TitleWithBody(
      title: t.generateView.style,
      action: const ResetButton(),
      child: GridView.builder(
        shrinkWrap: true,
        itemCount: 8,
        gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
            mainAxisSpacing: AppValues.kPadding / 2,
            crossAxisSpacing: AppValues.kPadding / 2,
            maxCrossAxisExtent: 140),
        itemBuilder: (context, index) => const _StyleWidget(),
      ),
    );
  }
}

class _StyleWidget extends StatelessWidget {
  const _StyleWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return const CircleAvatar();
  }
}
