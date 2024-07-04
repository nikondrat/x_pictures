import 'package:collection/collection.dart';
import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class ProfileView extends StatelessWidget {
  const ProfileView({super.key});

  @override
  Widget build(BuildContext context) {
    final List<String> tabs = [
      t.profile.pack,
      t.profile.img,
      t.profile.video,
    ];

    final List<PackModel> packs = [
      PackModel(title: 'Pack 1', length: 10, progress: 6, urls: [
        'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
        'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
        'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
        'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      ]),
      PackModel(title: 'Pack 1', length: 10, progress: 6, urls: [
        'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
        'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
        'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
        'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      ]),
    ];

    return Scaffold(
      body: AppBody(
        builder: (windowWidth, windowHeight, windowSize) {
          return SafeArea(
            child: SingleChildScrollView(
              child: Padding(
                  padding: HorizontalSpacing.centered(windowWidth) +
                      const EdgeInsets.symmetric(vertical: AppValues.kPadding),
                  child: Column(
                    children: [
                      ProfileInfoWidget(
                        name: 'Kary Filatova',
                        email: 'filyapel@yandex.ru',
                        url:
                            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
                        onTap: () => router.goNamed(AppViews.settingsView),
                      ),
                      const Gap(AppValues.kPadding),
                      Container(
                          decoration: const BoxDecoration(
                              color: AppColors.kSecondaryAdditionallyColor),
                          child: Row(
                              children: tabs.mapIndexed((index, title) {
                            return Expanded(
                                child: CustomTabWidget(
                                    isSelected: index == 0,
                                    title: title,
                                    onTap: () {}));
                          }).toList())),
                      if (packs.isNotEmpty) const Gap(AppValues.kPadding),
                      packs.isEmpty
                          ? IntrinsicHeight(
                              child: GestureDetector(
                                onTap: () {},
                                child: Image.asset(
                                  Assets.images.banner2.path,
                                  fit: BoxFit.contain,
                                ),
                              ),
                            )
                          : Column(
                              crossAxisAlignment: CrossAxisAlignment.stretch,
                              children: packs
                                  .map((e) => PackItem(
                                        pack: e,
                                      ))
                                  .toList()),
                    ],
                  )),
            ),
          );
        },
      ),
    );
  }
}
