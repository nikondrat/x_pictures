import 'package:cached_network_image/cached_network_image.dart';
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
        physics: const NeverScrollableScrollPhysics(),
        shrinkWrap: true,
        itemCount: 8,
        gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
            mainAxisSpacing: AppValues.kPadding / 2,
            crossAxisSpacing: AppValues.kPadding / 2,
            maxCrossAxisExtent: 100),
        itemBuilder: (context, index) => const _StyleWidget(),
      ),
    );
  }
}

class _StyleWidget extends StatelessWidget {
  const _StyleWidget();

  @override
  Widget build(BuildContext context) {
    return const CircleAvatar(
      backgroundImage: CachedNetworkImageProvider(
          'https://i.artfile.ru/2880x1800_957873_[www.ArtFile.ru].jpg'),
    );
  }
}
