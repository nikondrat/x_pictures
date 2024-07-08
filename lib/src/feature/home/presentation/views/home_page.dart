import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:x_pictures/src/data.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CustomScrollView(
        slivers: <Widget>[
          // const SliverToBoxAdapter(
          //   child: AppBarHomeView(),
          // ),
          SliverToBoxAdapter(
            child: SizedBox(
              height: 40.h,
            ),
          ),

          // LinkedIn
          const SliverToBoxAdapter(
            child: LinkedinListItems(),
          ),
          SliverToBoxAdapter(
            child: SizedBox(
              height: 20.h,
            ),
          ),
          // Hair Style
          const SliverToBoxAdapter(
            child: HairStyleListItems(),
          ),
          SliverToBoxAdapter(
            child: SizedBox(
              height: 20.h,
            ),
          ),
          // Tatto
          const SliverToBoxAdapter(
            child: TattoListItems(),
          ),
          SliverToBoxAdapter(
            child: SizedBox(
              height: 20.h,
            ),
          ),
          // Decades
          const SliverToBoxAdapter(
            child: DecadesListItems(),
          ),
          SliverToBoxAdapter(
            child: SizedBox(
              height: 30.h,
            ),
          ),
        ],
      ),
    );
  }
}
