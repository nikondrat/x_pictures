import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class BackgroundsView extends StatelessWidget {
  const BackgroundsView({super.key});

  @override
  Widget build(BuildContext context) {
    final Map<String, List<PackModel>> packs = {
      t.backgrounds.types.trending.title: [
        PackModel(
            id: 0,
            title: t.backgrounds.types.trending.types.sunset,
            description: '',
            category: '',
            images: []),
      ],
      t.backgrounds.types.colors.title: []
    };

    // final List<BackgroundSectionModel> sections = [
    //   BackgroundSectionModel(title: t.backgrounds.types.trending.title, items: [
    //     PackModel(
    //         title: t.backgrounds.types.trending.types.sunset,
    //         subTitle: '',
    //         data: [],
    //         description: '',
    //         url: 'https://pixy.org/src2/600/6001827.jpg'),
    //     PackModel(
    //         title: t.backgrounds.types.trending.types.moon,
    //         subTitle: '',
    //         data: [],
    //         description: '',
    //         url: 'https://i.ytimg.com/vi/4m_9sw_FDp4/maxresdefault.jpg'),
    //     PackModel(
    //         title: t.backgrounds.types.trending.types.beach,
    //         subTitle: '',
    //         data: [],
    //         description: '',
    //         url:
    //             'https://i.pinimg.com/originals/3f/82/b9/3f82b9b47fc3ac7852d8ead18c4ff134.jpg'),
    //     PackModel(
    //         title: t.backgrounds.types.trending.types.forest,
    //         subTitle: '',
    //         data: [],
    //         description: '',
    //         url:
    //             'https://img3.fonwall.ru/o/hw/tree-nature-forest-branch-tnln.jpeg?auto=compress&amp;fit=resize&amp;w=500&amp;display=thumb&amp;nsfw=false'),
    //     PackModel(
    //         title: t.backgrounds.types.trending.types.paris,
    //         subTitle: '',
    //         data: [],
    //         description: '',
    //         url: 'https://i.artfile.ru/2560x1600_1523474_[www.ArtFile.ru].jpg'),
    //     PackModel(
    //         title: t.backgrounds.types.trending.types.mountains,
    //         subTitle: '',
    //         data: [],
    //         description: '',
    //         url:
    //             'https://baldezh.top/uploads/posts/2021-03/1617213064_60-p-oboi-gori-kavkaza-63.jpg'),
    //   ]),
    //   BackgroundSectionModel(title: t.backgrounds.types.colors.title, items: [
    //     PackModel(
    //         title: t.backgrounds.types.colors.types.white,
    //         subTitle: '',
    //         data: [],
    //         description: '',
    //         url:
    //             'https://bogatyr.club/uploads/posts/2023-06/1686919599_bogatyr-club-p-belie-abstraktnie-oboi-foni-vkontakte-1.jpg'),
    //     PackModel(
    //         title: t.backgrounds.types.colors.types.black,
    //         subTitle: '',
    //         data: [],
    //         description: '',
    //         url:
    //             'https://furman.top/uploads/posts/2023-08/1690975784_furman-top-p-chernii-ekran-zastavka-oboi-77.jpg'),
    //     PackModel(
    //         title: t.backgrounds.types.colors.types.blue,
    //         subTitle: '',
    //         data: [],
    //         description: '',
    //         url:
    //             'https://www.pixel-creation.com/wp-content/uploads/blue-gradient-wallpaper-85-images.jpg'),
    //   ]),
    //   BackgroundSectionModel(title: t.backgrounds.types.texture.title, items: [
    //     PackModel(
    //         title: t.backgrounds.types.texture.types.wood,
    //         subTitle: '',
    //         data: [],
    //         description: '',
    //         url:
    //             'https://i.pinimg.com/originals/89/c3/be/89c3beddf3c836e9b04430020d9cf32b.jpg'),
    //     PackModel(
    //         title: t.backgrounds.types.texture.types.marble,
    //         subTitle: '',
    //         data: [],
    //         description: '',
    //         url:
    //             'https://furman.top/uploads/posts/2022-07/1656785464_18-furman-top-p-zolotoi-mramor-tekstura-krasivo-18.jpg'),
    //     PackModel(
    //         title: t.backgrounds.types.texture.types.concrete,
    //         subTitle: '',
    //         data: [],
    //         description: '',
    //         url:
    //             'https://abrakadabra.fun/uploads/posts/2021-12/1639637668_1-abrakadabra-fun-p-tekstura-betonnaya-stena-1.jpg'),
    //   ])
    // ];

    final textTheme = Theme.of(context).textTheme;

    return Scaffold(
      appBar: AppBar(
        title: Text(
          t.backgrounds.title,
          style: textTheme.bodyMedium!.copyWith(
            fontWeight: FontWeight.w700,
          ),
        ),
      ),
      body: ListView(
        padding: const EdgeInsets.only(
            left: AppValues.kPadding, top: AppValues.kPadding),
        children: packs.entries.map((e) {
          return BackgroundSection(
            title: e.key,
            packs: e.value,
            onTap: (model) {
              router.goNamed(AppViews.imageWithBackground,
                  extra: {'model': model});
            },
          );
        }).toList(),
      ),
    );
  }
}
