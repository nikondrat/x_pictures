import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class GenerateStyles extends StatelessWidget {
  const GenerateStyles({super.key});

  @override
  Widget build(BuildContext context) {
    final GenerateViewStore store = Provider.of<GenerateViewStore>(context);

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
        itemBuilder: (context, index) {
          return Observer(
            builder: (_) => GestureDetector(
                onTap: () {
                  store.setSelectedStyle(index);
                },
                child: _StyleWidget(
                  isSelected: store.selectedStyle == index,
                )),
          );
        },
      ),
    );
  }
}

class _StyleWidget extends StatelessWidget {
  final bool isSelected;
  const _StyleWidget({required this.isSelected});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final ColorScheme colorScheme = themeData.colorScheme;

    return Container(
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        border: isSelected
            ? Border.all(color: colorScheme.primary, width: 4)
            : null,
        image: const DecorationImage(
            fit: BoxFit.cover,
            image: CachedNetworkImageProvider(
                'https://i.artfile.ru/2880x1800_957873_[www.ArtFile.ru].jpg')),
      ),
    );
  }
}
